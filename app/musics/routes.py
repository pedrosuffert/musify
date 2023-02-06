from fastapi import APIRouter, UploadFile
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, update, delete

from app.helpers import filter_empty_keys
from app.musics.schemas import AddMusicSchema, UpdateMusicSchema
from database.connection import async_session
from database.models import Music

router = APIRouter()


@router.post("/")
async def add_music(schema: AddMusicSchema):
    with async_session as session:
        new_music = Music()
        new_music.name = schema.name
        new_music.lyrics = schema.lyrics
        new_music.language = schema.language
        new_music.artist_id = schema.artist_id
        new_music.album_id = schema.album_id
        await session.add(new_music)
    return ORJSONResponse(new_music.as_json())


@router.post("/{music_id}/upload")
async def create_upload_file(music_id: int, file: UploadFile):
    async with async_session as session:
        await session.execute(
            update(Music).where(Music.id == music_id).values(clip=await file.read())
        )
        return {"filename": file.filename}


@router.get("/")
async def get_musics():
    async with async_session as session:
        musics = (await session.execute(select(Music))).scalars().all()
    return ORJSONResponse([music.as_json() for music in musics], status_code=200)


@router.post("/{music_id}")
async def update_music(music_id: int, schema: UpdateMusicSchema):
    async with async_session as session:
        values = {
            "name": schema.name,
            "lyrics": schema.lyrics,
            "language": schema.language,
        }
        filter_empty_keys(values)
        await session.execute(
            update(Music).where(Music.id == music_id).values(**values)
        )
    return ORJSONResponse(
        {"msg": "Music updated successfully", "status": 200}, status_code=200
    )


@router.delete("/{music_id}")
async def delete_music(music_id: int):
    async with async_session as session:
        await session.execute(delete(Music).where(Music.id == music_id))
    return ORJSONResponse(
        {"msg": "Music deleted successfully", "status": 200}, status_code=200
    )
