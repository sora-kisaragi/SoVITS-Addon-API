from app.db.database import engine, SessionLocal
from app.models import Character, Preset

# モデル定義からテーブルを作成
def init_db():
    """データベースの初期化とテーブル作成を行う"""
    # importしたモデルクラスが自動的にBase.metadataに登録される
    from app.db.database import Base
    Base.metadata.create_all(bind=engine)
    
    # 初期データの投入が必要な場合はここに追加
    create_initial_data()

def create_initial_data():
    """初期データの作成（必要な場合）"""
    db = SessionLocal()
    
    # 初期データがまだ存在しない場合のみ投入
    if db.query(Character).count() == 0:
        # サンプルキャラクターの作成
        alice = Character(
            name="Alice",
        )
        db.add(alice)
        db.commit()
        db.refresh(alice)
        
        # サンプルプリセットの作成
        default_preset = Preset(
            character_id=alice.id,
            name="Default",
            speed=1.0,
            emotion=0.5,
            voice_model="model_a"
        )
        db.add(default_preset)
        db.commit()
        
        # デフォルトプリセットを設定
        alice.default_preset_id = default_preset.id
        db.commit()
        
    db.close()

# スクリプト直接実行時にDBを初期化
if __name__ == "__main__":
    print("データベースを初期化しています...")
    init_db()
    print("データベース初期化が完了しました")
