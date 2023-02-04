from datetime import date, timedelta
from aiohttp import ClientSession
from sqlalchemy.ext.asyncio.session import async_session
from sqlalchemy.future import select
from sqlalchemy import delete

from database.models import Genres
from database.connection import async_session

async def create_genres(name: str):
    async with async_session() as session:
        session.add(Genres(name=name))
        await session.commit()

async def delete_genres(Genres_id: int):
    async with async_session() as session:
        await session.execute(delete(Genres).where(Genres.id==Genres_id))
        await session.commit()

async def list_genres():
    async with async_session() as session:
        result = await session.execute(select(Genres))
        return result.scalars().all()
    
async def get_by_id(genres_id):
    async with async_session() as session:
        result = await session.execute(select(Genres).where(Genres.id==genres_id))
        return result.scalar()