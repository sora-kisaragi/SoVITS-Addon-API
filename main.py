from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import character_router
from app.routers import preset_router
from app.db.database import init_db

# アプリケーションのインスタンス作成
app = FastAPI(
    title="SoVITS Addon API",
    description="GPT-SoVITSを用いた音声生成API",
    version="0.1.0"
)

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
app.include_router(preset_router.router)

@app.get("/")
async def root():
    return {"message": "SoVITS Addon API"}