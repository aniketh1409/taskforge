from app.db.session import SessionLocal
from app.core.constants import JOB_STATUS_RUNNING
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
    finally:
        db.close()