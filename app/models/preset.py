from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import DateTime
from sqlalchemy.orm import relationship

from app.db.database import Base


class Preset(Base):
    """プリセット情報モデル"""
    
    __tablename__ = "presets"
    
    id = Column(Integer, primary_key=True, index=True)
    character_id = Column(Integer, ForeignKey("characters.id"))
    name = Column(String(255), nullable=False)
    speed = Column(Float, nullable=False)
    emotion = Column(Float, nullable=False)
    voice_model = Column(String(255), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # リレーションシップの定義
    # 外部キーを明示的に指定
    character = relationship("Character", back_populates="presets", foreign_keys=[character_id])