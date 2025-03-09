import taskiq_fastapi
from taskiq import InMemoryBroker
from taskiq_nats import PullBasedJetStreamBroker
from taskiq_redis import RedisAsyncResultBackend

from fastapi_app.settings import settings

broker = PullBasedJetStreamBroker(
    settings.nats_urls.split(","),
    queue="fastapi_app_queue",
).with_result_backend(
    RedisAsyncResultBackend(settings.redis_url),
)

# Actually, you can remove this line and test agains real
# broker. Which is more preferable in some cases.
if settings.env.lower() == "pytest":
    broker = InMemoryBroker()


taskiq_fastapi.init(broker, "fastapi_app.__main__:get_app")
