from fastapi import FastAPI

from fastapi_app.lifetime import shutdown, startup
from fastapi_app.routes import router


def get_app() -> FastAPI:
    app = FastAPI(
        title="FastAPI-app",
        docs_url="/swagger",
    )

    app.add_event_handler("startup", startup(app))
    app.add_event_handler("shutdown", shutdown(app))

    app.include_router(router)

    return app
