from fastapi import FastAPI

from fastapi_app import lifespan
from fastapi_app.routes import router


def get_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI-app",
        docs_url="/docs",
        lifespan=lifespan.lifespan,
    )

    app.include_router(router)

    return app
