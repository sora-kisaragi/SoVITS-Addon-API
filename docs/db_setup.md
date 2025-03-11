# **データベーステーブル作成SQL**
```sql
-- プリセットテーブル作成
CREATE TABLE presets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 一意のID
    name TEXT NOT NULL,                    -- キャラクター名
    speed REAL DEFAULT 1.0,                -- 話速 (デフォルト 1.0)
    pitch REAL DEFAULT 1.0,                -- 声の高さ (デフォルト 1.0)
    emotion TEXT DEFAULT '{}',             -- 感情設定 (デフォルト 空のJSON)
    is_deleted INTEGER DEFAULT 0,          -- 削除フラグ (デフォルト 0)
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,  -- 作成日
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP -- 更新日
);

-- 音声ファイルテーブル（生成音声を一時保存）
CREATE TABLE generated_audio (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- 一意のID
    preset_id INTEGER NOT NULL,            -- 対応するプリセットID
    file_path TEXT NOT NULL,               -- 音声ファイルのパス
    generated_at DATETIME DEFAULT CURRENT_TIMESTAMP, -- 生成日時
    FOREIGN KEY (preset_id) REFERENCES presets(id) -- プリセットIDとの関連
);

-- インデックスを作成して検索効率を向上
CREATE INDEX idx_preset_name ON presets (name);
CREATE INDEX idx_generated_audio_preset_id ON generated_audio (preset_id);
```

## **CSVフォーマットの項目（初期プリセット）**  
初期プリセットとして **キャラクターごとの音声設定** を登録するため、以下のような項目を設定します。  

| 項目名         | 型      | 説明 | 例 |
|---------------|--------|----------------------|----------------|
| `name`        | TEXT   | キャラクター名（プリセット名） | `"Alice"` |
| `speed`       | REAL   | 話速（1.0が標準、0.5で遅く、2.0で速い） | `1.2` |
| `pitch`       | REAL   | 声の高さ（1.0が標準、0.8で低く、1.2で高い） | `1.0` |
| `emotion`     | TEXT   | 感情設定（JSONで複数表現を格納） | `{"happy":0.8, "sad":0.2}` |
| `is_deleted`  | INTEGER | 削除フラグ（0=有効, 1=削除済） | `0` |

**補足**
- **`emotion` のJSONフォーマット**  
   - `{"happy": 0.8, "sad": 0.2}` のように複数の感情パラメータを持てるようにする。  
   - 必須ではなく、空でもよい。  
- **`is_deleted` を使って削除管理**  
   - 削除フラグが `1` のプリセットは通常非表示にする（完全削除はしない）。  
   - 復元機能を考慮する場合は `is_deleted=0` に変更すればよい。

---

### **CSVインポート手順**
1. **CSVファイルの準備**  
   以下のようなCSVファイルを作成します：
   ```csv
   name,speed,pitch,emotion,is_deleted
   Alice,1.2,1.0,"{\"happy\":0.8, \"sad\":0.2}",0
   Bob,1.0,0.9,"{}",0
   ```

2. **CSVをインポートするSQL**  
   SQLiteでは、CSVを直接インポートするためには以下のコマンドを使います：
   ```sql
   .mode csv
   .import /path/to/your/file.csv presets
   ```

3. **インポート後の確認**  
   インポート後にプリセットが正しく追加されたことを確認します：
   ```sql
   SELECT * FROM presets;
   ```

### **手動で音声ファイルを削除する方法**
生成された音声ファイルは定期的に手動で削除する予定なので、以下の方法で削除できます：

1. **不要な音声ファイルを削除**  
   ファイルシステムで生成された音声ファイルを手動で削除します。
   例：
   ```bash
   rm /tmp/generated_audio/{uuid}.wav
   ```

2. **`generated_audio` テーブルからも削除**  
   音声ファイルを削除した後、対応するレコードも削除します：
   ```sql
   DELETE FROM generated_audio WHERE file_path = '/tmp/generated_audio/{uuid}.wav';
   ```

---