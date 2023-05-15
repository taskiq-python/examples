import aiohttp_deps
from aiohttp import web

from aiohttp_app import lifetime
from aiohttp_app.routes import router

app = web.Application()
app.on_startup.extend(
    [
        aiohttp_deps.init,
        aiohttp_deps.setup_swagger(
            swagger_ui_url="/swagger",
        ),
    ]
)
app.cleanup_ctx.extend([lifetime.setup_db, lifetime.setup_taskiq])

app.add_routes(router)
