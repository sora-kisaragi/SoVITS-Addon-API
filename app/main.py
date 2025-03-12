from fastapi import FastAPI
# 絶対インポートに戻す（プロジェクト構造に合わせる）
from app.routers import character_router

app = FastAPI(
    title="SoVITS Add-on API",
    description="GPT-SoVITSを操作するためのAPIサービス",
    version="0.1.0"
)

# ルーターの登録
app.include_router(character_router.router)

@app.get("/")
def read_root():
    return {"message": "Welcome to SoVITS Add-on API"}

# デバッグ用に追加（開発時のみ使用）
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000)
