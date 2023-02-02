import asyncio

from database.connection import db_engine
from database.models import Base


async def recreate_database():
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


if __name__ == '__main__':
    asyncio.run(recreate_database())