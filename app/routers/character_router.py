from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate, CharacterList
from app.services.character_service import CharacterService

router = APIRouter(
    prefix="/characters",
    tags=["characters"]
)

@router.get("", response_model=CharacterList)
def get_characters(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """キャラクター一覧を取得するエンドポイント
    
    Args:
        skip: スキップする件数
        limit: 取得する最大件数
        db: データベースセッション
        
    Returns:
        キャラクター一覧
    """
    characters = CharacterService.get_characters(db, skip, limit)
    return {"characters": characters}

@router.get("/{character_id}", response_model=CharacterResponse)
def get_character(character_id: int, db: Session = Depends(get_db)):
    """キャラクター詳細を取得するエンドポイント
    
    Args:
        character_id: キャラクターID
        db: データベースセッション
        
    Returns:
        キャラクター詳細情報
    """
    character = CharacterService.get_character(db, character_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    return character

@router.post("", response_model=CharacterResponse, status_code=status.HTTP_201_CREATED)
def create_character(character: CharacterCreate, db: Session = Depends(get_db)):
    """キャラクターを作成するエンドポイント
    
    Args:
        character: 作成するキャラクター情報
        db: データベースセッション
        
    Returns:
        作成されたキャラクター情報
    """
    return CharacterService.create_character(db, character)

@router.put("/{character_id}", response_model=CharacterResponse)
def update_character(character_id: int, character: CharacterUpdate, db: Session = Depends(get_db)):
    """キャラクターを更新するエンドポイント
    
    Args:
        character_id: 更新するキャラクターID
        character: 更新内容
        db: データベースセッション
        
    Returns:
        更新後のキャラクター情報
    """
    updated_character = CharacterService.update_character(db, character_id, character)
    if not updated_character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
    return updated_character

@router.delete("/{character_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_character(character_id: int, db: Session = Depends(get_db)):
    """キャラクターを削除するエンドポイント
    
    Args:
        character_id: 削除するキャラクターID
        db: データベースセッション
    """
    result = CharacterService.delete_character(db, character_id)
    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Character with id {character_id} not found"
        )
