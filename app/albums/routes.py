from datetime import datetime

from fastapi import APIRouter, UploadFile
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, update, delete

from app.albums.schemas import AddAlbumSchema, UpdateAlbumSchema
from app.helpers import filter_empty_keys
from database.connection import async_session
from database.models import Album

router = APIRouter()


@router.post("/")
async def add(schema: AddAlbumSchema):
    async with async_session as session:
        new_album = Album()
        new_album.name = schema.name
        new_album.release_date = (
            datetime.fromisoformat(schema.release_date)
            if schema.release_date
            else datetime.utcnow()
        )
        new_album.artist_id = schema.artist_id
        session.add(new_album)
        await session.commit()
    return ORJSONResponse(new_album.as_json(), status_code=200)


@router.post("/{album_id}/upload")
async def create_upload_file(album_id: int, file: UploadFile):
    async with async_session as session:
        await session.execute(
            update(Album).where(Album.id == album_id).values(cover=await file.read())
        )
        await session.commit()
    return {"filename": file.filename}


@router.get("/{album_id}")
async def get_album(album_id: int):
    async with async_session as session:
        album = (
            (await session.execute(select(Album).where(Album.id == album_id)))
            .scalars()
            .first()
        )
    return ORJSONResponse(album.as_json(), status_code=200)


@router.get("/")
async def get_album():
    async with async_session as session:
        albums = (await session.execute(select(Album))).scalars()
    return ORJSONResponse([album.as_json() for album in albums], status_code=200)


@router.put("/{album_id}")
async def update_album(album_id: int, schema: UpdateAlbumSchema):
    async with async_session as session:
        values = {
            "name": schema.name,
            "release_date": datetime.fromisoformat(schema.release_date)
            if schema.release_date
            else datetime.utcnow(),
        }
        filter_empty_keys(values)
        await session.execute(
            update(Album).where(Album.id == album_id).values(**values)
        )
        await session.commit()
    return ORJSONResponse(
        {"id": album_id, "msg": "Album updated successfully", "status": 200},
        status_code=200,
    )


@router.delete("/{album_id}")
async def delete_album(album_id: int):
    async with async_session as session:
        await session.execute(delete(Album).where(Album.id == album_id))
        await session.commit()
    return ORJSONResponse(
        {"message": "Album deleted successfully", "status": 200}, status_code=200
    )
