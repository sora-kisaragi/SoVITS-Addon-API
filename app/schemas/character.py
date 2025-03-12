from typing import List, Optional
from pydantic import BaseModel

class CharacterBase(BaseModel):
    """キャラクターの基本情報を表すベースモデル"""
    name: str
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    voice_model_path: str

class CharacterCreate(CharacterBase):
    """キャラクター作成リクエスト用モデル"""
    pass

class CharacterUpdate(BaseModel):
    """キャラクター更新リクエスト用モデル"""
    name: Optional[str] = None
    description: Optional[str] = None
    avatar_url: Optional[str] = None
    voice_model_path: Optional[str] = None

class CharacterResponse(CharacterBase):
    """キャラクターのレスポンス用モデル"""
    id: int
    
    class Config:
        orm_mode = True

class CharacterList(BaseModel):
    """キャラクター一覧のレスポンス用モデル"""
    characters: List[CharacterResponse]
