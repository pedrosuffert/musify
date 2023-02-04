from pydantic import BaseModel


class AddGenresSchema(BaseModel):
    name: str
    description: str