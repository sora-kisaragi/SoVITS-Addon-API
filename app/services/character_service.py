from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.character import Character
from app.schemas.character import CharacterCreate, CharacterUpdate

class CharacterService:
    """キャラクター関連のビジネスロジックを扱うサービスクラス"""
    
    @staticmethod
    def get_characters(db: Session, skip: int = 0, limit: int = 100) -> List[Character]:
        """キャラクター一覧を取得する

        Args:
            db: データベースセッション
            skip: スキップする件数
            limit: 取得する最大件数

        Returns:
            キャラクター一覧
        """
        return db.query(Character).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_character(db: Session, character_id: int) -> Optional[Character]:
        """キャラクター詳細を取得する

        Args:
            db: データベースセッション
            character_id: キャラクターID

        Returns:
            キャラクター情報、存在しない場合はNone
        """
        result = db.query(Character).filter(Character.id == character_id).first()

        return result
    
    @staticmethod
    def create_character(db: Session, character: CharacterCreate) -> Character:
        """キャラクターを作成する

        Args:
            db: データベースセッション
            character: 作成するキャラクター情報

        Returns:
            作成されたキャラクター
        """
        db_character = Character(**character.dict())
        db.add(db_character)
        db.commit()
        db.refresh(db_character)
        return db_character
    
    @staticmethod
    def update_character(db: Session, character_id: int, character: CharacterUpdate) -> Optional[Character]:
        """キャラクターを更新する

        Args:
            db: データベースセッション
            character_id: 更新するキャラクターID
            character: 更新情報

        Returns:
            更新されたキャラクター、存在しない場合はNone
        """
        db_character = CharacterService.get_character(db, character_id)
        if not db_character:
            return None
        
        update_data = character.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_character, key, value)
        
        db.commit()
        db.refresh(db_character)
        return db_character
    
    @staticmethod
    def delete_character(db: Session, character_id: int) -> bool:
        """キャラクターを削除する

        Args:
            db: データベースセッション
            character_id: 削除するキャラクターID

        Returns:
            削除に成功した場合はTrue、存在しない場合はFalse
        """
        db_character = CharacterService.get_character(db, character_id)
        if not db_character:
            return False
        
        db.delete(db_character)
        db.commit()
        return True
