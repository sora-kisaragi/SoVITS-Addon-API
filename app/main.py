from fastapi import FastAPI
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
