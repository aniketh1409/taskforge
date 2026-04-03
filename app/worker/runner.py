from app.db.session import SessionLocal
from app.core.constants import JOB_STATUS_RUNNING, JOB_STATUS_FAILED, JOB_STATUS_SUCCEEDED
from app.db.models import Job


def process_job(job_id: str) -> None:
    db = SessionLocal()
    try:
        job = db.get(Job, job_id)
        if job is None:
            return
        job.status = JOB_STATUS_RUNNING
        db.commit()
        db.refresh(job)

        try:
            job.result = {
                "Message" : "Working fine!",
                "Author" : "Aniketh"
            }
            job.error = None
            job.status = JOB_STATUS_SUCCEEDED
            db.commit()

        except Exception as e:
            job.status = JOB_STATUS_FAILED
            job.error = str(e)
            db.commit()
        
    finally:
        db.close()