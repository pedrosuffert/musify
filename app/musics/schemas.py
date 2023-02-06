from typing import Optional

from pydantic import BaseModel


class AddMusicSchema(BaseModel):
    name: str
    artist_id: int
    album_id: int
    lyrics: Optional[str]
    language: Optional[str]


class UpdateMusicSchema(BaseModel):
    name: Optional[str] = None
    lyrics: Optional[str] = None
    language: Optional[str] = None
