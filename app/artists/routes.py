from datetime import datetime

from fastapi import APIRouter, UploadFile
from fastapi.responses import ORJSONResponse
from sqlalchemy import select, update, delete

from app.artists.schemas import AddArtistSchema, UpdateArtistSchema
from app.helpers import filter_empty_keys
from database.connection import async_session
from database.models import Artist

router = APIRouter()


@router.post("/")
async def add_artist(schema: AddArtistSchema):
    async with async_session as session:
        new_artist = Artist()
        new_artist.name = schema.name
        new_artist.birth_date = (
            datetime.fromisoformat(schema.birth_date)
            if schema.birth_date
            else datetime.utcnow()
        )
        session.add(new_artist)
        await session.commit()
    return ORJSONResponse(new_artist.as_json(), status_code=200)


@router.post("/{artist_id}/upload")
async def create_upload_file(artist_id: int, file: UploadFile):
    async with async_session as session:
        await session.execute(
            update(Artist).where(Artist.id == artist_id).values(photo=await file.read())
        )
        await session.commit()
    return {
        "id": artist_id,
        "filename": file.filename,
        "msg": "Photo uploaded successfully",
        "status": 200,
    }


@router.get("/{artist_id}")
async def get_album(artist_id: int):
    async with async_session as session:
        album = (
            (await session.execute(select(Artist).where(Artist.id == artist_id)))
            .scalars()
            .first()
        )
    return ORJSONResponse(album.as_json(), status_code=200)


@router.get("/")
async def get_artists():
    async with async_session as session:
        artists = (await session.execute(select(Artist))).scalars().all()
    return ORJSONResponse([artist.as_json() for artist in artists], status_code=200)


@router.put("/{artist_id}")
async def update_artist(artist_id: int, schema: UpdateArtistSchema):
    async with async_session as session:
        values = {
            "name": schema.name,
            "birth_date": datetime.fromisoformat(schema.birth_date)
            if schema.birth_date
            else datetime.utcnow(),
            "photo": schema.photo,
        }
        filter_empty_keys(values)
        await session.execute(
            update(Artist).where(Artist.id == artist_id).values(**values)
        )
        await session.commit()
    return ORJSONResponse(
        {"id": artist_id, "msg": "Artist updated successfully", "status": 200},
        status_code=200,
    )


@router.delete("/{artist_id}")
async def delete_artist(artist_id: int):
    async with async_session as session:
        await session.execute(delete(Artist).where(Artist.id == artist_id))
        await session.commit()
    return ORJSONResponse(
        {"msg": "Artist deleted successfully", "status": 200}, status_code=200
    )
