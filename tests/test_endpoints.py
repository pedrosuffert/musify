from datetime import datetime

import pytest
from httpx import AsyncClient

from database.connection import async_session
from database.models import Artist, Album, Music


async def create_random_artist():
    async with async_session as session:
        artist = Artist(name="The Weekend")
        session.add(artist)
        await session.flush()
        await session.refresh(artist)
        await session.commit()
        return artist


async def create_random_album(artist_id):
    async with async_session as session:
        album = Album(name="After Hours")
        album.artist_id = artist_id
        session.add(album)
        await session.flush()
        await session.refresh(album)
        await session.commit()
        return album


async def create_random_music(artist_id, album_id):
    async with async_session as session:
        music = Music(name="Blinding Lights")
        music.artist_id = artist_id
        music.album_id = album_id
        session.add(music)
        await session.flush()
        await session.refresh(music)
        await session.commit()
        return music


@pytest.mark.asyncio
async def test_add_artist():
    async with AsyncClient(timeout=None) as ac:
        json = {
            "name": "The Weekend",
            "birth_date": datetime.isoformat(datetime.utcnow()),
        }
        response = await ac.post("http://localhost:9000/artists/", json=json)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["name"] == json["name"]
        assert json_response["birth_date"] == json["birth_date"]


@pytest.mark.asyncio
async def test_upload_artist_photo():
    artist = await create_random_artist()
    file = {"file": ("test.jpg", "test content")}
    async with AsyncClient(timeout=None) as ac:
        response = await ac.post(
            f"http://localhost:9000/artists/{artist.id}/upload", files=file
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_artists():
    async with AsyncClient(timeout=None) as ac:
        response = await ac.get("http://localhost:9000/artists/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_artist():
    artist = await create_random_artist()
    async with AsyncClient(timeout=None) as ac:
        json = {
            "name": "Xama",
        }
        response = await ac.post(
            f"http://localhost:9000/artists/{artist.id}", json=json
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_artist():
    artist = await create_random_artist()
    async with AsyncClient(timeout=None) as ac:
        response = await ac.delete(f"http://localhost:9000/artists/{artist.id}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_album():
    artist = await create_random_artist()
    async with AsyncClient(timeout=None) as ac:
        json = {
            "name": "After Hours",
            "artist_id": artist.id,
            "release_date": datetime.isoformat(datetime.utcnow()),
        }
        response = await ac.post("http://localhost:9000/albums/", json=json)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response["name"] == json["name"]
        assert json_response["release_date"] == json["release_date"]


@pytest.mark.asyncio
async def test_upload_artist_photo():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    file = {"file": ("test.jpg", "test content")}
    async with AsyncClient(timeout=None) as ac:
        response = await ac.post(
            f"http://localhost:9000/albums/{album.id}/upload", files=file
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_albums():
    async with AsyncClient(timeout=None) as ac:
        response = await ac.get("http://localhost:9000/albums/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_album():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    async with AsyncClient(timeout=None) as ac:
        json = {
            "name": "Zodiaco",
            "release_date": datetime.isoformat(datetime.utcnow()),
        }
        response = await ac.post(f"http://localhost:9000/albums/{album.id}", json=json)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_album():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    async with AsyncClient(timeout=None) as ac:
        response = await ac.delete(f"http://localhost:9000/albums/{album.id}")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_music():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    json = {
        "name": "Blinding Lights",
        "artist_id": artist.id,
        "album_id": album.id,
    }
    async with AsyncClient(timeout=None) as ac:
        response = await ac.post("http://localhost:9000/musics/", json=json)
        assert response.status_code == 200
        assert response.json() == {"id": 1, "title": "test"}


@pytest.mark.asyncio
async def test_upload_music_photo():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    music = await create_random_music(artist.id, album.id)
    file = {"file": ("test.jpg", "test content")}
    async with AsyncClient(timeout=None) as ac:
        response = await ac.post(
            f"http://localhost:9000/musics/{music.id}/upload", files=file
        )
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_musics():
    async with AsyncClient(timeout=None) as ac:
        response = await ac.get("http://localhost:9000/musics/")
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_music():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    music = await create_random_music(artist.id, album.id)
    async with AsyncClient(timeout=None) as ac:
        json = {
            "name": "Leao",
        }
        response = await ac.post(f"http://localhost:9000/musics/{music.id}", json=json)
        assert response.status_code == 200


@pytest.mark.asyncio
async def test_delete_music():
    artist = await create_random_artist()
    album = await create_random_album(artist.id)
    music = await create_random_music(artist.id, album.id)
    async with AsyncClient(timeout=None) as ac:
        response = await ac.delete(f"http://localhost:9000/musics/{music.id}")
        assert response.status_code == 200
