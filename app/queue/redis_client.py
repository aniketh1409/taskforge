import redis

from app.core.config import settings
from app.core.constants import JOB_QUEUE_NAME


redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses = True)
'''
created a redis client object using configured url, similar to how we did engine for postgres
'''


def enqueue_job(job_id: str) -> None:
    redis_client.rpush(JOB_QUEUE_NAME, job_id)