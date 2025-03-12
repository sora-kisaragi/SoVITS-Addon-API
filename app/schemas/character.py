from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

class CharacterBase(BaseModel):
    """キャラクターの基本情報を表すベースモデル"""
    name: str
    default_preset_id: Optional[int] = None


class CharacterCreate(CharacterBase):
    """キャラクター作成リクエスト用モデル"""
    pass


class CharacterUpdate(BaseModel):
    """キャラクター更新リクエスト用モデル"""
    name: Optional[str] = None
    default_preset_id: Optional[int] = None


class CharacterResponse(CharacterBase):
    """キャラクターのレスポンス用モデル"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class CharacterList(BaseModel):
    """キャラクター一覧のレスポンス用モデル"""
    items: List[CharacterResponse]
    total: int
    skip: int
    limit: int