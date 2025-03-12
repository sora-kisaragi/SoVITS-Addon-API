from app.db.database import SessionLocal, create_tables
from app.models.character import Character
from app.models.preset import Preset

def initialize_db():
    """
    データベースの完全な初期化を行う
    1. テーブルの作成
    2. 初期データの投入
    """
    # テーブルの作成
    create_tables()
    
    # 初期データの投入
    create_initial_data()

def create_initial_data():
    """初期データの作成"""
    # 明示的にテーブルを作成して確実に存在するようにする
    from app.db.database import Base, engine
    
    try:
        # テーブルの作成を強制的に実行
        Base.metadata.create_all(bind=engine)
        
        # テーブルが存在するか確認
        from sqlalchemy import inspect
        inspector = inspect(engine)
        
        # テーブル名を出力（デバッグ用）
        print(f"作成されたテーブル: {inspector.get_table_names()}")
        
        # SessionLocalを直接インポート
        from app.db.database import SessionLocal
        db = SessionLocal()
        
        try:
            # 初期データを作成
            print("初期データを作成しています...")
            
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
            
            print("初期データの作成が完了しました")
            return True
        except Exception as e:
            db.rollback()
            print(f"初期データ作成エラー: {e}")
            return False
        finally:
            db.close()
    except Exception as e:
        print(f"テーブル作成エラー: {e}")
        return False


# スクリプト直接実行時にDBを初期化
if __name__ == "__main__":
    print("データベースを初期化しています...")
    initialize_db()
    print("データベース初期化が完了しました")