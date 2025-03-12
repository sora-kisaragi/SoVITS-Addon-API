from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.database import Base

class Preset(Base):
    """プリセット情報モデル"""
    
    __tablename__ = "presets"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    character_id = Column(Integer, ForeignKey("characters.id"), nullable=False)
    name = Column(String, nullable=False)
    speed = Column(Float, nullable=False, default=1.0)
    emotion = Column(Float, nullable=False, default=0.5)
    voice_model = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # リレーションシップ
    character = relationship("Character", back_populates="presets", foreign_keys=[character_id])
