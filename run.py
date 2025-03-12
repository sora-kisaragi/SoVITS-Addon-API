import uvicorn
import sys
import os
import traceback

# デバッグ情報を表示
print("現在の作業ディレクトリ:", os.getcwd())
print("Pythonパス:", sys.path)

try:
    # プロジェクトルートをPythonパスに追加（インポート問題を解決）
    sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
    
    print("アプリケーション起動中...")
    if __name__ == "__main__":
        uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
except Exception as e:
    print("エラーが発生しました:")
    print(traceback.format_exc())
