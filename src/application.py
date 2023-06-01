import mimetypes
from fastapi import FastAPI
from .containers import Container
from . import endpoints


def create_app() -> FastAPI:
    container = Container()

    app = FastAPI()
    app.container = container
    app.include_router(endpoints.router)

    mimetypes.init()  # init mime types

    return app


app = create_app()
