from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddAlbumSchema(BaseModel):
    name: str
    artist_id: int
    release_date: Optional[datetime] = None


class UpdateAlbumSchema(BaseModel):
    name: Optional[str] = None
    release_date: Optional[datetime] = None
