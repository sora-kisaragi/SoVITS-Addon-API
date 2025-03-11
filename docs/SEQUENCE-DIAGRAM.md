# SoVITS Addon API シーケンス図

このドキュメントでは、SoVITS Addon APIの主要な処理フローをシーケンス図で説明します。

## 音声生成フロー (/generate エンドポイント)

```mermaid
sequenceDiagram
    participant Client as クライアント
    participant API as APIサーバー
    participant Engine as 音声生成エンジン (GPT-SoVITS)
    participant Preset as プリセット管理
    participant Discord as Discord Webhook (通知)
    
    Client->>API: /generate (キャラ名, テキスト, 設定)
    API->>Preset: プリセット取得 (キャラ名)
    Preset-->>API: プリセット設定
    API->>Engine: 音声生成リクエスト (テキスト, 設定)
    Engine-->>API: 生成音声データ (WAV)
    API-->>Client: 音声ファイル送信 (WAV)
    
    alt 通知が設定されている場合
        API->>Discord: Webhook通知 (生成完了メッセージ)
    end
```

## 解説
1. クライアントが ```/generate API``` を呼び出し、キャラクター名とテキストを送信。
2. API サーバーは プリセット管理システム から キャラクターごとの設定 を取得。
3. 取得した設定とリクエストの情報をもとに、音声生成エンジン（GPT-SoVITS）にリクエスト送信。
4. エンジンが音声データを生成し、API に WAV ファイルを返す。
5. API はクライアントに音声ファイルを返却。
6. 通知が設定されている場合のみ、Discord Webhook に通知を送信。
