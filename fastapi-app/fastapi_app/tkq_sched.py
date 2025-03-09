from taskiq import TaskiqScheduler
from taskiq.schedule_sources import LabelScheduleSource
from taskiq_redis import RedisScheduleSource
from fastapi_app.settings import settings
from fastapi_app.tkq import broker


redis_source = RedisScheduleSource(settings.redis_url)


scheduler = TaskiqScheduler(
    broker,
    [
        # Dynamic schedule source. To add tasks dynamically.
        redis_source,
        # Label schedule source. To schedule tasks with labels.
        LabelScheduleSource(broker),
    ],
)
