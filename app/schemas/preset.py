from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class PresetBase(BaseModel):
    """プリセットの基本情報を定義するベースモデル"""
    name: str = Field(..., description="プリセット名")
    character_id: int = Field(..., description="関連するキャラクターID")
    description: Optional[str] = Field(None, description="プリセットの説明")
    # SoVITSのパラメータ
    speaker_id: int = Field(..., description="話者ID")
    noise_scale: float = Field(0.6, description="ノイズスケール", ge=0.0, le=1.0)
    noise_scale_w: float = Field(0.8, description="ノイズスケールW", ge=0.0, le=1.0)
    length_scale: float = Field(1.0, description="長さスケール", gt=0.0)
    sdp_ratio: float = Field(0.2, description="SDP比率", ge=0.0, le=1.0)
    # 追加パラメータがあれば追加


class PresetCreate(PresetBase):
    """プリセット作成時に使用するモデル"""
    pass


class PresetUpdate(BaseModel):
    """プリセット更新時に使用するモデル（すべてのフィールドがオプション）"""
    name: Optional[str] = Field(None, description="プリセット名")
    character_id: Optional[int] = Field(None, description="関連するキャラクターID")
    description: Optional[str] = Field(None, description="プリセットの説明")
    speaker_id: Optional[int] = Field(None, description="話者ID")
    noise_scale: Optional[float] = Field(None, description="ノイズスケール", ge=0.0, le=1.0)
    noise_scale_w: Optional[float] = Field(None, description="ノイズスケールW", ge=0.0, le=1.0)
    length_scale: Optional[float] = Field(None, description="長さスケール", gt=0.0)
    sdp_ratio: Optional[float] = Field(None, description="SDP比率", ge=0.0, le=1.0)


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