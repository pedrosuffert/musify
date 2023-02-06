from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from app.artists.routes import router as artists_router
from app.albums.routes import router as albums_router
from app.musics.routes import router as musics_router


def create_app():
    app = FastAPI()

    # noinspection PyUnusedLocal
    @app.route("/")
    async def home(request):
        return ORJSONResponse({})

    app.include_router(artists_router, prefix=f"/artists")
    app.include_router(albums_router, prefix=f"/albums")
    app.include_router(musics_router, prefix=f"/musics")

    return app
