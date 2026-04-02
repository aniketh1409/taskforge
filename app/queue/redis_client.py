import redis

from app.core.config import settings
from app.core.constants import JOB_QUEUE_NAME


redis_client = redis.Redis.from_url(settings.REDIS_URL, decode_responses = True)
'''
created a redis client object using configured url, similar to how we did engine for postgres
'''


def enqueue_job(job_id: str) -> None:
    redis_client.rpush(JOB_QUEUE_NAME, job_id)

def dequeue_job() -> str | None:
    item = redis_client.blpop(JOB_QUEUE_NAME, timeout = 5) #b -> blocking; if queue is empty worker waits (no hammering in a tight loop)

    if item is None:
        return None
    
    _, job_id = item #_ is a throwaway variable, here we are unpacking the tuple!
    return job_id
