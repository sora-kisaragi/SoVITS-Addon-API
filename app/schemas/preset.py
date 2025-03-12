from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PresetBase(BaseModel):
    """プリセットの基本情報を定義するベースモデル"""
    name: str = Field(..., description="プリセット名")
    character_id: int = Field(..., description="関連するキャラクターID")
    speed: float = Field(..., description="音声の速度")
    emotion: float = Field(..., description="感情の度合い")
    voice_model: str = Field(..., description="使用する音声モデル")


class PresetCreate(PresetBase):
    """プリセット作成時に使用するモデル"""
    pass


class PresetUpdate(BaseModel):
    """プリセット更新時に使用するモデル（すべてのフィールドがオプション）"""
    name: Optional[str] = Field(None, description="プリセット名")
    character_id: Optional[int] = Field(None, description="関連するキャラクターID")
    speed: Optional[float] = Field(None, description="音声の速度")
    emotion: Optional[float] = Field(None, description="感情の度合い")
    voice_model: Optional[str] = Field(None, description="使用する音声モデル")


class PresetInDBBase(PresetBase):
    """データベースから取得したプリセット情報のモデル"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Preset(PresetInDBBase):
    """API応答用のプリセットモデル"""
    pass


class PresetList(BaseModel):
    """プリセット一覧の応答モデル"""
    total: int
    items: List[Preset]