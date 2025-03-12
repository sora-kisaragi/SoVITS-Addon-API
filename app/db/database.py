from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import sys
import shutil
from dotenv import load_dotenv

# 環境変数の読み込み
load_dotenv()

# データベースURL（環境変数から取得、なければデフォルト値を使用）
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./sovits.db")

# SQLiteのDBファイルパスを取得する関数
def get_db_file_path():
    """
    SQLiteのDBファイルパスを取得する
    
    Returns:
        str: DBファイルパス（SQLite以外の場合はNone）
    """
    if SQLALCHEMY_DATABASE_URL.startswith("sqlite:///"):
        db_path = SQLALCHEMY_DATABASE_URL.replace("sqlite:///", "")
        # 相対パスの場合、./を除去
        if db_path.startswith("./"):
            db_path = db_path[2:]
        return db_path
    return None

# データベース初期化フラグを判定する関数
def should_init_db():
    """
    データベースを初期化すべきかどうかを判断する
    
    以下の条件で判断:
    1. 環境変数 INIT_DATABASE が設定されている場合はその値を使用
    2. コマンドライン引数に --init-db がある場合は初期化する
    3. SQLiteの場合、DBファイルが存在しなければ初期化する
    
    Returns:
        bool: 初期化すべきかどうか
    """
    # 1. 環境変数でのチェック
    env_init = os.getenv("INIT_DATABASE")
    if env_init is not None:
        return env_init.lower() in ("true", "1", "yes", "y")
    
    # 2. コマンドライン引数でのチェック
    if "--init-db" in sys.argv:
        return True
    if "--no-init-db" in sys.argv:
        return False
    
    # 3. SQLiteの場合、DBファイルの存在チェック
    db_path = get_db_file_path()
    if db_path:
        # DBファイルが存在しない場合のみ初期化
        return not os.path.exists(db_path)
    
    # デフォルトでは初期化しない
    return False

# データベースファイルを削除する関数
def remove_db_file():
    """
    SQLiteのデータベースファイルを削除する
    成功した場合はTrue、失敗または非SQLiteの場合はFalseを返す
    """
    db_path = get_db_file_path()
    if db_path and os.path.exists(db_path):
        try:
            os.remove(db_path)
            print(f"データベースファイルを削除しました: {db_path}")
            return True
        except Exception as e:
            print(f"データベースファイル削除エラー: {e}")
    return False

# 初期化フラグ
INIT_DATABASE = should_init_db()

# SQLAlchemyエンジンの作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# セッションローカルの作成
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# モデルのベースクラス
Base = declarative_base()

# データベーステーブルの基本初期化関数（テーブル作成のみ）
def create_tables():
    """
    データベースのテーブルを作成する
    """
    try:
        Base.metadata.create_all(bind=engine)
        print("データベーステーブルを作成しました")
        return True
    except Exception as e:
        print(f"データベーステーブル作成エラー: {e}")
        return False

# データベース初期化関数
def init_db():
    """
    初期化フラグに基づいてデータベースを初期化する
    テーブル作成と初期データ投入を行う
    """
    # 初期化フラグの状態を確認用に出力
    print(f"データベース初期化フラグ: {INIT_DATABASE}")
    
    if INIT_DATABASE:
        try:
            # 既存のDBファイルを削除
            remove_db_file()
            
            # 新しいセッションでテーブルを作成
            if create_tables():
                # テーブル作成成功後、初期データの投入
                from app.db.init_db import create_initial_data
                if create_initial_data():
                    print("データベースを初期化しました")
                    return True
                else:
                    print("初期データの投入に失敗したため、データベース初期化は不完全です")
                    return False
            else:
                print("テーブル作成に失敗したため、初期データは投入されませんでした")
                return False
        except Exception as e:
            print(f"データベース初期化エラー: {e}")
            return False
    else:
        print("データベースの初期化はスキップされました")
        return False

# データベースセッションの取得
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()