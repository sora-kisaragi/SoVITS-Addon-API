from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.schemas.preset import Preset, PresetList, PresetCreate, PresetUpdate
from app.services.preset_service import PresetService

# ルーターの初期化
router = APIRouter(
    prefix="/presets",
    tags=["presets"],
    responses={404: {"description": "プリセットが見つかりません"}},
)

# サービスのインスタンス化
preset_service = PresetService()


@router.get("/", response_model=PresetList)
def get_presets(
    skip: int = Query(0, ge=0, description="スキップする件数"),
    limit: int = Query(100, ge=1, le=100, description="取得する最大件数"),
    character_id: Optional[int] = Query(None, description="キャラクターIDでフィルタリング"),
    db: Session = Depends(get_db),
):
    """
    プリセット一覧を取得する
    
    - **skip**: スキップする件数（0以上）
    - **limit**: 取得する最大件数（1～100）
    - **character_id**: 特定のキャラクターに関連するプリセットのみを取得する場合に指定
    """
    return preset_service.get_presets(db, skip=skip, limit=limit, character_id=character_id)


@router.get("/{preset_id}", response_model=Preset)
def get_preset(
    preset_id: int = Path(..., ge=1, description="取得するプリセットのID"),
    db: Session = Depends(get_db),
):
    """
    指定IDのプリセットを取得する
    
    - **preset_id**: 取得するプリセットのID
    """
    return preset_service.get_preset(db, preset_id)


@router.post("/", response_model=Preset, status_code=201)
def create_preset(
    preset_data: PresetCreate,
    db: Session = Depends(get_db),
):
    """
    新しいプリセットを作成する
    
    - **preset_data**: 作成するプリセットのデータ
    """
    return preset_service.create_preset(db, preset_data)


@router.put("/{preset_id}", response_model=Preset)
def update_preset(
    preset_update: PresetUpdate,
    preset_id: int = Path(..., ge=1, description="更新するプリセットのID"),
    db: Session = Depends(get_db),
):
    """
    既存のプリセットを更新する
    
    - **preset_id**: 更新するプリセットのID
    - **preset_update**: 更新するプリセットのデータ
    """
    return preset_service.update_preset(db, preset_id, preset_update)


@router.delete("/{preset_id}", response_model=Preset)
def delete_preset(
    preset_id: int = Path(..., ge=1, description="削除するプリセットのID"),
    db: Session = Depends(get_db),
):
    """
    プリセットを削除する
    
    - **preset_id**: 削除するプリセットのID
    """
    return preset_service.delete_preset(db, preset_id)