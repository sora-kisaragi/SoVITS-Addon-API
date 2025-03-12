from sqlalchemy.orm import Session
from sqlalchemy import desc
from typing import List, Optional, Dict, Any
from app.models.preset import Preset
from app.schemas.preset import PresetCreate, PresetUpdate


class PresetRepository:
    """
    プリセット情報のデータベース操作を担当するリポジトリクラス
    """

    def get_presets(
        self, db: Session, *, skip: int = 0, limit: int = 100, character_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        プリセットの一覧を取得する

        Args:
            db: データベースセッション
            skip: スキップする件数
            limit: 取得する最大件数
            character_id: キャラクターIDでフィルタリングする場合に指定

        Returns:
            総件数とプリセット一覧を含む辞書
        """
        # クエリ作成
        query = db.query(Preset)
        
        # キャラクターIDでフィルタリング
        if character_id is not None:
            query = query.filter(Preset.character_id == character_id)
        
        # 総件数取得
        total = query.count()
        
        # データ取得（更新日時の降順）
        items = query.order_by(desc(Preset.updated_at)).offset(skip).limit(limit).all()
        
        return {"total": total, "items": items}

    def get_preset(self, db: Session, preset_id: int) -> Optional[Preset]:
        """
        指定されたIDのプリセットを取得する

        Args:
            db: データベースセッション
            preset_id: プリセットID

        Returns:
            プリセットオブジェクト。見つからない場合はNone
        """
        return db.query(Preset).filter(Preset.id == preset_id).first()

    def create_preset(self, db: Session, preset_data: PresetCreate) -> Preset:
        """
        新しいプリセットを作成する

        Args:
            db: データベースセッション
            preset_data: 作成するプリセットのデータ

        Returns:
            作成されたプリセットオブジェクト
        """
        # dictに変換し、モデルインスタンスを作成
        db_preset = Preset(**preset_data.dict())
        
        # データベースに追加
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        
        return db_preset

    def update_preset(
        self, db: Session, preset_id: int, preset_update: PresetUpdate
    ) -> Optional[Preset]:
        """
        既存のプリセットを更新する

        Args:
            db: データベースセッション
            preset_id: 更新するプリセットのID
            preset_update: 更新データ

        Returns:
            更新されたプリセットオブジェクト。プリセットが見つからない場合はNone
        """
        # 更新対象のプリセットを取得
        db_preset = self.get_preset(db, preset_id)
        if db_preset is None:
            return None

        # 更新データから辞書を作成（Noneの項目は除外）
        update_data = preset_update.dict(exclude_unset=True)
        
        # モデルを更新
        for field, value in update_data.items():
            setattr(db_preset, field, value)

        # データベースに反映
        db.add(db_preset)
        db.commit()
        db.refresh(db_preset)
        
        return db_preset

    def delete_preset(self, db: Session, preset_id: int) -> Optional[Preset]:
        """
        プリセットを削除する

        Args:
            db: データベースセッション
            preset_id: 削除するプリセットのID

        Returns:
            削除されたプリセットオブジェクト。プリセットが見つからない場合はNone
        """
        # 削除対象のプリセットを取得
        db_preset = self.get_preset(db, preset_id)
        if db_preset is None:
            return None

        # データベースから削除
        db.delete(db_preset)
        db.commit()
        
        return db_preset