from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db.init_db import init_db
from app.routers import character_router

app = FastAPI(
    title="SoVITS Addon API",
    description="GPT-SoVITSを用いた音声生成API",
    version="0.1.0"
)

# アプリケーション起動時にデータベースを初期化
@app.on_event("startup")
async def startup_db_client():
    init_db()

# CORSミドルウェアの設定
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 本番環境では適切に制限してください
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ルーターの登録
app.include_router(character_router.router)


@app.get("/")
async def root():
    return {"message": "SoVITS Addon API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)