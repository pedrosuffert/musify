from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel


class AddArtistSchema(BaseModel):
    name: str
    birth_date: Optional[str] = None


class UpdateArtistSchema(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[str] = None
    photo: Optional[str] = None
