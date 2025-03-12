from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Character(Base):
    """キャラクター情報モデル"""
    
    __tablename__ = "characters"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False, index=True)
    default_preset_id = Column(Integer, ForeignKey("presets.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # リレーションシップ
    presets = relationship("Preset", back_populates="character", foreign_keys="Preset.character_id")
    default_preset = relationship("Preset", foreign_keys=[default_preset_id], post_update=True)
