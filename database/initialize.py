import asyncio
import logging

from app.factory import create_app


from database.connection import async_session, db_engine
from database.models import Base


async def flush_everything():
    logging.info("Re-creating all tables...")
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def initialize_application(flush_database: bool):
    if flush_database:
        await flush_everything()
    async with async_session as session:
        await session.commit()


async def main():
    create_app()
    await initialize_application(flush_database=True)
    print("Initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())
