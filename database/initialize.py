import asyncio
import logging
from datetime import datetime

from app.factory import create_app


from database.connection import async_session, db_engine
from database.models import Base, Artist, Album, Music

init = [
    {
        "model": Artist,
        "items": [
            {
                "name": "Harry Styles",
                "birth_date": datetime.fromisoformat("1994-02-01"),
            },
            {"name": "Matuê", "birth_date": datetime.fromisoformat("1993-10-11")},
            {
                "name": "Imagine Dragons",
                "birth_date": datetime.fromisoformat("1987-07-14"),
            },
            {"name": "Shakira", "birth_date": datetime.fromisoformat("1977-02-02")},
            {"name": "The Weekend", "birth_date": datetime.fromisoformat("1990-02-16")},
        ],
    },
    {
        "model": Album,
        "items": [
            {
                "name": "Fine Line",
                "release_date": datetime.fromisoformat("2019-12-13"),
                "artist_id": 1,
            },
            {
                "name": "Máquina do Tempo",
                "release_date": datetime.fromisoformat("2019-09-10"),
                "artist_id": 2,
            },
            {
                "name": "Evolve",
                "release_date": datetime.fromisoformat("2017-06-23"),
                "artist_id": 3,
            },
            {
                "name": "World Cup",
                "release_date": datetime.fromisoformat("2010-05-28"),
                "artist_id": 4,
            },
            {
                "name": "After Hours",
                "release_date": datetime.fromisoformat("2020-03-20"),
                "artist_id": 5,
            },
        ],
    },
    {
        "model": Music,
        "items": [
            {
                "name": "Watermelon Sugar",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 1,
                "album_id": 1,
            },
            {
                "name": "As It Was",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 1,
                "album_id": 1,
            },
            {
                "name": "Kenny G",
                "clip": None,
                "lyrics": None,
                "language": "portuguese",
                "artist_id": 2,
                "album_id": 2,
            },
            {
                "name": "Quer Voar",
                "clip": None,
                "lyrics": None,
                "language": "portuguese",
                "artist_id": 2,
                "album_id": 2,
            },
            {
                "name": "Believer",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 3,
                "album_id": 3,
            },
            {
                "name": "Radioactive",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 3,
                "album_id": 3,
            },
            {
                "name": "Waka Waka",
                "clip": None,
                "lyrics": None,
                "language": "spanish",
                "artist_id": 4,
                "album_id": 4,
            },
            {
                "name": "La La La",
                "clip": None,
                "lyrics": None,
                "language": "spanish",
                "artist_id": 4,
                "album_id": 4,
            },
            {
                "name": "Blinding Lights",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 5,
                "album_id": 5,
            },
            {
                "name": "Die For You",
                "clip": None,
                "lyrics": None,
                "language": "english",
                "artist_id": 5,
                "album_id": 5,
            },
        ],
    },
]


async def flush_everything():
    logging.info("Re-creating all tables...")
    async with db_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def initialize_application(flush_database: bool):
    if flush_database:
        await flush_everything()
    async with async_session as session:
        for config in init:
            model = config["model"]
            logging.info(f"Creating objects for {model}")
            for values in config["items"]:
                new_obj = model()
                for key, value in values.items():
                    setattr(new_obj, key, value)
                session.add(new_obj)
            await session.commit()


async def main():
    create_app()
    await initialize_application(flush_database=True)
    print("Initialized successfully")


if __name__ == "__main__":
    asyncio.run(main())
