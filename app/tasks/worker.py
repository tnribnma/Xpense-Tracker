from arq import create_pool
from arq.connections import RedisSettings
from app.core.config import settings
from app.tasks.email_jobs import send_budget_alert_email

async def startup(ctx):
    print("Worker started up!")

class WorkerSettings:
    functions = [send_budget_alert_email]
    on_startup = startup
    redis_settings = RedisSettings.from_dsn(settings.REDIS_URL)