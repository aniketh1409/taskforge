from fastapi import APIRouter, HTTPException, Depends
from app.core.constants import (JOB_STATUS_SUCCEEDED, 
                                JOB_STATUS_RUNNING, 
                                JOB_STATUS_FAILED, 
                                JOB_STATUS_QUEUED, 
                                TASK_TYPE_DEMO_SLEEP_ECHO)
from uuid import UUID, uuid4
from app.api.schemas.jobs import RequestModel, ResponseModel
from app.db.session import get_db
from app.db.models import Job
from sqlalchemy.orm import Session


router = APIRouter()

@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/list-status")
def display_status_list():
    return { "Success" : JOB_STATUS_SUCCEEDED,
            "Failure": JOB_STATUS_FAILED,
            "Running": JOB_STATUS_RUNNING,
            "Queued": JOB_STATUS_QUEUED}


@router.post("/jobs", response_model = ResponseModel)
def create_job(request: RequestModel, db : Session = Depends(get_db)):
    generate_uuid = uuid4()
    job = Job(id = str(generate_uuid), 
              status = JOB_STATUS_QUEUED, 
              task_type = request.task_type, 
              payload = request.payload)
    db.add(job)
    db.commit()
    db.refresh(job)

    new_job = ResponseModel(
        job_id = UUID(job.id), 
        status = job.status,
        task_type = job.task_type,
        payload = job.payload
        )

    return new_job

@router.get("/jobs/{job_id}", response_model = ResponseModel)
def retrieve_job(job_id: UUID, db: Session = Depends(get_db)):
    job = db.get(Job, str(job_id))
    if job is None:
        raise HTTPException(status_code = 404, detail = "Job not found")
    
    return ResponseModel(
        job_id = UUID(job.id), 
        status = job.status,
        task_type = job.task_type,
        payload = job.payload
        )

@router.get("/jobs", response_model = list[ResponseModel]) #type hint to define a rule which means that ResponseModel must be of type list!
def retrieve_all_jobs(db : Session = Depends(get_db)):
    jobs = db.query(Job).all()

    return [
        ResponseModel(
        job_id = UUID(job.id), 
        status = job.status,
        task_type = job.task_type,
        payload = job.payload
        )
        for job in jobs
    ]

