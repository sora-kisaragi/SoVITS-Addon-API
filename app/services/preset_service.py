from typing import List, Dict, Any, Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.schemas.preset import PresetCreate, PresetUpdate
from app.repositories.preset_repository import PresetRepository


class PresetService:
    """
    プリセット情報のビジネスロジックを担当するサービスクラス
    """

    def __init__(self):
        """
        PresetServiceの初期化
        """
        self.repository = PresetRepository()

    def get_presets(
        self, db: Session, skip: int = 0, limit: int = 100, character_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        プリセット一覧を取得する

        Args:
            db: データベースセッション
            skip: スキップする件数
            limit: 取得する最大件数
            character_id: キャラクターIDでフィルタリングする場合に指定

        Returns:
            総件数とプリセット一覧を含む辞書
        """
        return self.repository.get_presets(db, skip=skip, limit=limit, character_id=character_id)

    def get_preset(self, db: Session, preset_id: int):
        """
        指定されたIDのプリセットを取得する

        Args:
            db: データベースセッション
            preset_id: プリセットID

        Returns:
            プリセットオブジェクト

        Raises:
            HTTPException: プリセットが見つからない場合
        """
        preset = self.repository.get_preset(db, preset_id)
        if preset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プリセットID {preset_id} は見つかりません",
            )
        return preset

    def create_preset(self, db: Session, preset_data: PresetCreate):
        """
        新しいプリセットを作成する

        Args:
            db: データベースセッション
            preset_data: 作成するプリセットのデータ

        Returns:
            作成されたプリセットオブジェクト
        """
        # キャラクターの存在確認などの追加バリデーションがある場合はここに実装
        # 例: self._validate_character_exists(db, preset_data.character_id)

        return self.repository.create_preset(db, preset_data)

    def update_preset(self, db: Session, preset_id: int, preset_update: PresetUpdate):
        """
        既存のプリセットを更新する

        Args:
            db: データベースセッション
            preset_id: 更新するプリセットのID
            preset_update: 更新データ

        Returns:
            更新されたプリセットオブジェクト

        Raises:
            HTTPException: プリセットが見つからない場合
        """
        updated_preset = self.repository.update_preset(db, preset_id, preset_update)
        if updated_preset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プリセットID {preset_id} は見つかりません",
            )
        return updated_preset

    def delete_preset(self, db: Session, preset_id: int):
        """
        プリセットを削除する

        Args:
            db: データベースセッション
            preset_id: 削除するプリセットのID

        Returns:
            削除されたプリセットオブジェクト

        Raises:
            HTTPException: プリセットが見つからない場合
        """
        deleted_preset = self.repository.delete_preset(db, preset_id)
        if deleted_preset is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"プリセットID {preset_id} は見つかりません",
            )
        return deleted_preset

    # 必要に応じて追加のヘルパーメソッドや検証ロジックを実装
    # def _validate_character_exists(self, db: Session, character_id: int):
    #     # キャラクターの存在確認ロジック
    #     pass