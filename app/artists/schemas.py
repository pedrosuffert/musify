from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AddArtistSchema(BaseModel):
    name: str
    birth_date: Optional[datetime] = None


class UpdateArtistSchema(BaseModel):
    name: Optional[str] = None
    birth_date: Optional[datetime] = None
