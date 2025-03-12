# SoVITS Addon API

SoVITS Addon API は、GPT-SoVITS の拡張として、キャラクターごとのカスタム音声生成機能を提供する RESTful API です。  
このプロジェクトでは、テキストを入力することで高品質な音声（WAV形式）を生成し、リアルタイムストリーミングや  
Discord Webhook を用いた通知機能も実装しています。

---

## 目次

- [SoVITS Addon API](#sovits-addon-api)
  - [目次](#目次)
  - [概要](#概要)
  - [機能](#機能)
  - [インストール](#インストール)
    - [前提条件](#前提条件)
    - [セットアップ手順](#セットアップ手順)
  - [設定](#設定)
  - [API エンドポイント](#api-エンドポイント)
    - [/generate エンドポイント（音声生成）](#generate-エンドポイント音声生成)
    - [/stream エンドポイント（ストリーミング音声）](#stream-エンドポイントストリーミング音声)
  - [使用例](#使用例)
    - [音声生成の例](#音声生成の例)
    - [音声ストリーミングの例](#音声ストリーミングの例)
  - [開発タスク](#開発タスク)
  - [ライセンス](#ライセンス)
  - [コントリビュート](#コントリビュート)
  - [お問い合わせ](#お問い合わせ)

---

## 概要

SoVITS Addon API は、GPT-SoVITS エンジンを拡張し、以下の機能を提供します。

- **音声生成**: テキストを入力すると WAV 形式の音声ファイルを生成
- **リアルタイムストリーミング**: HTTP チャンク転送を用いて生成音声をリアルタイム配信
- **キャラクター別プリセット管理**: 各キャラクターに対応したプリセット（例：「happy」「sad」など）の設定を適用
- **設定管理**: キャラクターごとのデフォルト設定（プリセット、話速、感情）を変更可能
- **Discord 通知**: オプションで Webhook URL を指定すると、生成完了時に Discord へ通知

---

## 機能

- **音声生成**  
  テキストから高品質な音声（WAV）を生成し、直接ファイルとして返却します。
  
- **リアルタイムストリーミング**  
  HTTP のチャンク転送エンコーディングを用いて、生成した音声をリアルタイムに配信します。
  
- **カスタムプリセット管理**  
  キャラクターごとに異なるプリセット（話速、感情、使用音声モデル）を設定できます。
  
- **設定変更**  
  WebUI 経由で各キャラクターのデフォルト設定を変更できます。
  
- **Discord Webhook 通知**  
  指定された Webhook URL に対して、音声生成完了時に通知を送信します。
  
- **SQLite データベース利用**  
  プリセットやキャラクターの設定情報は、メタデータ（作成日時、更新日時）付きで SQLite に保存されます。

---

## インストール

### 前提条件

- Python 3.9 以上 3.11 未満
- SQLite
- CUDA 対応 GPU（リアルタイム音声生成のため）
- GPT-SoVITSが動作する環境

### セットアップ手順

1. **リポジトリのクローン**
    ```bash
    git clone https://github.com/sora-kisaragi/sovits-addon-api.git
    cd sovits-addon-api
    ```

2. **GPT-SoVITSのダウンロード**
    ```bash
    curl -L "https://huggingface.co/lj1995/GPT-SoVITS-windows-package/resolve/main/GPT-SoVITS-beta.7z?download=true" -o ./downloads/GPT-SoVITS-beta.7z
    SEVEN_ZIP="/c/Program Files/7-Zip/7z.exe"
    mkdir -p ./GPT-SoVITS
    "$SEVEN_ZIP" x ./downloads/GPT-SoVITS-beta.7z -o"$(cygpath -w ./GPT-SoVITS)" -y
    ```

3. **仮想環境の作成 & アクティベート**
    ```bash
    python -m venv venv
    source venv/bin/activate  # Windows の場合: venv\Scripts\activate
    ```

4. **依存ライブラリのインストール**
    ```bash
    pip install -r requirements.txt
    ```

5. **データベースのセットアップ**
    - 提供された SQL スクリプトを実行してテーブルを作成します。
    - CSV インポートで初期プリセットデータを登録してください。

6. **環境変数の設定**
    - プロジェクトルートに `.env` ファイルを作成し、以下のように設定します。
    ```ini
    # .env の例
    CUDA_VISIBLE_DEVICES=0
    DISCORD_DEFAULT_WEBHOOK_URL=https://discord.com/api/webhooks/your-webhook-id/your-webhook-token
    DATABASE_URL=sqlite:///./sovits.db
    ```

---

## 設定

環境変数や設定ファイルを用いて、システムの各種パラメータ（GPUデバイス、Discord Webhook、DBパスなど）を設定します。  
詳細は `.env` ファイルをご参照ください。

---

## API エンドポイント

詳細な仕様は [API仕様書](./docs/API-SPEC.md)を確認してください。

### /generate エンドポイント（音声生成）

- **目的:**  
  テキストから音声（WAV ファイル）を生成し、直接 WAV データをレスポンスとして返します。
  
- **HTTP メソッド:**  
  `POST`
  
- **リクエストパラメータ (JSON):**

  | パラメータ    | 型      | 必須  | 説明 |
  |---------------|---------|-------|--------------------------------------------------------------|
  | text          | string  | 必須  | 生成する音声の原文テキスト                                     |
  | character     | string  | 必須  | 使用するキャラクター名（プリセットはこのキャラクターのものから選択） |
  | preset        | string  | オプション | 使用するプリセット名（省略時はキャラクターのデフォルト設定を適用）   |
  | speed         | number  | オプション | 話速（プリセット値を上書き可能）                                |
  | emotion       | string  | オプション | 感情パラメータ（プリセット値を上書き可能）                        |
  | webhook_url   | string  | オプション | Discord Webhook の URL（指定時のみ通知を送信）                  |

- **レスポンス:**
  - **成功時:**  
    - `Content-Type: audio/wav` を設定し、生成した WAV ファイルを直接返却。
  - **エラー時:**  
    ```json
    {
      "status": "error",
      "error_code": 400,
      "message": "Detailed error message here"
    }
    ```

---

### /stream エンドポイント（ストリーミング音声）

- **目的:**  
  テキストから生成された音声を、HTTP チャンク転送エンコーディングによりリアルタイムでストリーミング再生します。
  
- **HTTP メソッド:**  
  `POST`
  
- **リクエストパラメータ:**  
  `/generate` と同様のパラメータを使用します。

- **レスポンス:**
  - **成功時:**  
    - `Content-Type: audio/wav` および `Transfer-Encoding: chunked` を用いて WAV データをストリーミング送信。
  - **ストリーミング終了後:**  
    - リクエストに `webhook_url` が指定されている場合、Discord への通知を送信します。
  - **エラー時:**  
    同様の JSON エラーレスポンスを返します。

---


## 使用例

### 音声生成の例
```bash
curl -X POST http://localhost:5000/generate \
  -H "Content-Type: application/json" \
  -d '{
        "text": "こんにちは！",
        "character": "Alice",
        "preset": "happy",
        "speed": 1.2,
        "emotion": "happy",
        "webhook_url": "https://discord.com/api/webhooks/..."
      }' --output output.wav
```

### 音声ストリーミングの例
```bash
curl -X POST http://localhost:5000/stream \
  -H "Content-Type: application/json" \
  -d '{
        "text": "ストリーミングのテストです。",
        "character": "Bob",
        "preset": "neutral",
        "webhook_url": "https://discord.com/api/webhooks/..."
      }'
```

---

## 開発タスク

詳細な開発タスクは [Development Task List](./DEVELOPMENT_TASKS.md) を参照してください。

---

## ライセンス

このプロジェクトは MIT License のもとで公開されています。詳細は [LICENSE](./LICENSE) ファイルをご覧ください。

---

## コントリビュート

コントリビュートは大歓迎です！リポジトリをフォークし、プルリクエストを送ってください。バグ修正や機能拡張の提案もお待ちしております。

---

## お問い合わせ

ご質問や問題がある場合は、GitHub の Issue をご利用いただくか、プロジェクトメンテナにご連絡ください。