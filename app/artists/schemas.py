from pydantic import BaseModel


class AddArtistSchema(BaseModel):
    name: str
    description: str
    image: str