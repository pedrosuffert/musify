import os
from dotenv import load_dotenv

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker


load_dotenv()

pg_user = os.getenv('PG_USER')
pg_password = os.getenv('PG_PASSWORD')
pg_port = os.getenv('PG_PORT')
pg_db = os.getenv('PG_DB')


db_engine = create_async_engine(f"postgresql+asyncpg://{pg_user}:{pg_password}@localhost:{pg_port}/{pg_db}")
async_session = sessionmaker(db_engine, class_=AsyncSession)