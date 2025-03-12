# **API 仕様書**

## **1. /generate エンドポイント（音声生成）**

- **目的:**  
  テキストから音声（WAV ファイル）を生成し、直接 WAV データをレスポンスとして返します。

- **HTTP メソッド:**  
  `POST`

- **リクエストパラメータ (JSON):**
  | パラメータ    | 型       | 必須 | 説明 |
  |--------------|----------|------|------|
  | `text`       | string   | 必須 | 生成する音声の原文テキスト |
  | `character`  | string   | 必須 | 使用するキャラクター名 |
  | `preset`     | string   | オプション | 使用するプリセット名（キャラクターごとのプリセット一覧から選択）。 |
  | `speed`      | number   | オプション | 話速。プリセットの値を上書き可能。 |
  | `emotion`    | number   | オプション | 感情パラメータ。プリセットの値を上書き可能。 |
  | `webhook_url`| string   | オプション | Discord Webhook の URL。指定された場合、生成完了後に通知を送信。 |

- **レスポンス:**  
  成功時は HTTP レスポンスとして直接生成した WAV ファイルを返します。  
  エラー時は以下の JSON 形式のエラーレスポンスを返します。
  ```json
  {
    "status": "error",
    "error_code": 400,
    "message": "Detailed error message here"
  }
  ```

---

## **2. /stream エンドポイント（ストリーミング音声）**

- **目的:**  
  テキストから生成された音声を HTTP チャンク転送エンコーディングによりリアルタイムでストリーミング再生します。

- **HTTP メソッド:**  
  `POST`

- **リクエストパラメータ (JSON):**  
  `/generate` と同じパラメータを使用します。  
  ※ `text`, `character`, `preset`, `speed`, `emotion`, `webhook_url` を指定可能です。

- **レスポンス:**  
  HTTP のチャンク転送エンコーディングを用いて、生成された音声データ（WAV）をリアルタイムに送信します。  
  ストリーミング終了後、`webhook_url` が指定されていれば Discord への通知を行います。

---

## **3. /presets エンドポイント（キャラクターごとのプリセット一覧取得）**

- **目的:**  
  システムに登録されているキャラクターごとのプリセット一覧を取得するためのエンドポイントです。

- **HTTP メソッド:**  
  `GET`

- **レスポンス (JSON):**
  キャラクターごとにプリセットが分類され、以下の形式で返します。
  ```json
  {
    "presets": {
      "Alice": [
        {
          "name": "happy",
          "speed": 1.2,
          "emotion": "happy",
          "voice_model": "model_A.pth"
        },
        {
          "name": "sad",
          "speed": 0.9,
          "emotion": "sad",
          "voice_model": "model_A.pth"
        }
      ],
      "Bob": [
        {
          "name": "neutral",
          "speed": 1.0,
          "emotion": "neutral",
          "voice_model": "model_B.pth"
        }
      ]
    }
  }
  ```

---

## **4. /settings エンドポイント（キャラクターごとの設定変更）**

- **目的:**  
  WebUI からデフォルトのプリセットおよび関連パラメータ（話速・感情など）をキャラクターごとに変更するためのエンドポイントです。

- **HTTP メソッド:**  
  `POST`

- **リクエストパラメータ (JSON):**
  キャラクター別の設定を変更可能にします。例：
  ```json
  {
    "character": "Alice",
    "default_preset": "happy",
    "default_speed": 1.0,
    "default_emotion": "neutral"
  }
  ```
  ※ 必要に応じて、キャラクターごとに異なるデフォルト設定を適用できます。

- **レスポンス:**  
  正常時は以下のような JSON を返します。
  ```json
  {
    "status": "updated"
  }
  ```
  エラー時はエラーメッセージを含む JSON を返します。

---

## **5. エラーハンドリング**

- **エラーレスポンス形式 (全エンドポイント共通):**
  ```json
  {
    "status": "error",
    "error_code": 400,
    "message": "Detailed error message here"
  }
  ```
  ※ 追加情報についての要望は特にないため、この形式で統一します。

---

## **6. /logs エンドポイント**

- **備考:**  
  ログは WebUI 上でのみ表示し、API 経由でのログ取得エンドポイントは実装しません。

---

## **7. 通知について（Discord Webhook）**

- **仕様:**  
  - `/generate` および `/stream` エンドポイントで、リクエストに `webhook_url` が指定された場合のみ、音声生成完了後に Discord Webhook を使用して通知を送信します。
  - 通知メッセージの例:
    ```json
    {
      "content": "音声生成が完了しました 🎙️",
      "embeds": [
        {
          "title": "音声情報",
          "fields": [
            { "name": "キャラクター", "value": "Alice", "inline": true },
            { "name": "プリセット", "value": "happy", "inline": true },
            { "name": "速度", "value": "1.2", "inline": true },
            { "name": "感情", "value": "happy", "inline": true }
          ]
        }
      ]
    }
    ```
  ※ この通知は Webhook URL がリクエストに含まれる場合にのみ行います。

---
