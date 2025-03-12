from typing import List, Optional
from pydantic import BaseModel

class CharacterBase(BaseModel):
    """キャラクターの基本情報を表すベースモデル"""


class CharacterCreate(CharacterBase):
    """キャラクター作成リクエスト用モデル"""


class CharacterUpdate(BaseModel):
    """キャラクター更新リクエスト用モデル"""


class CharacterResponse(BaseModel):
    """キャラクターのレスポンス用モデル"""

class CharacterList(BaseModel):
    """キャラクター一覧のレスポンス用モデル"""

