import taskiq_aiohttp
from taskiq_nats import NatsBroker
from taskiq_redis import RedisAsyncResultBackend

from aiohttp_app.settings import settings

broker = NatsBroker(
    servers=settings.nats_urls.split(","),
    queue="aiohttp_app",
).with_result_backend(
    RedisAsyncResultBackend(
        settings.redis_url,
        result_ex_time=200,
    )
)

taskiq_aiohttp.init(broker, "aiohttp_app.__main__:app")
