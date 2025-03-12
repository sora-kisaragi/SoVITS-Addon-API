import uvicorn
import sys
import argparse
from app.db.database import init_db

def main():
    """
    アプリケーションのエントリーポイント
    コマンドライン引数の処理とアプリケーションの起動を行う
    """
    # 引数パーサーの設定
    parser = argparse.ArgumentParser(description="SoVITS Addon API サーバー")
    parser.add_argument("--host", default="127.0.0.1", help="ホストアドレス")
    parser.add_argument("--port", type=int, default=8000, help="ポート番号")
    parser.add_argument("--reload", action="store_true", help="リロードモードの有効化")
    parser.add_argument("--init-db", action="store_true", help="データベースを強制的に初期化")
    parser.add_argument("--no-init-db", action="store_true", help="データベースの初期化をスキップ")
    
    # コマンドライン引数の解析
    args = parser.parse_args()
    
    # アプリケーション起動前にデータベースの初期化チェック
    init_db()
    
    # FastAPIアプリケーション起動
    print(f"サーバーを起動します: http://{args.host}:{args.port}")
    uvicorn.run("main:app", host=args.host, port=args.port, reload=args.reload)

if __name__ == "__main__":
    main()