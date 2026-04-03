from fastapi import FastAPI
from app.api.routes.jobs import router
from app.core.config import settings
from app.db.session import Base, engine
import app.db.models
from app.queue.redis_client import dequeue_job
from app.worker.runner import process_job

#creating the fastapi app object
app = FastAPI(title = settings.APP_NAME)

#including the routing object to attach endpoints from the jobs router into the app
app.include_router(router)

#creates those tables inside postgres that sqlalchemy knows about, will only know if model module is imported
Base.metadata.create_all(bind = engine)

def main(): #main always runs (pulls from queue and processes using worker's process job)
    while 1:
        job_id = dequeue_job()
        if job_id is None:
            continue
        else:
            process_job(job_id)
            
if __name__ == "__main__":
    main()