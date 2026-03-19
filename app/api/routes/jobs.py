from fastapi import APIRouter, HTTPException
from app.core.constants import JOB_STATUS_SUCCEEDED, JOB_STATUS_RUNNING, JOB_STATUS_FAILED, JOB_STATUS_QUEUED, TASK_TYPE_DEMO_SLEEP_ECHO
from pydantic import BaseModel
from uuid import UUID, uuid4


router = APIRouter()

jobs_store = {}


@router.get("/health")
def health_check():
    return {"status": "ok"}

@router.get("/list-status")
def display_status_list():
    return { "Success" : JOB_STATUS_SUCCEEDED,
            "Failure": JOB_STATUS_FAILED,
            "Running": JOB_STATUS_RUNNING,
            "Queued": JOB_STATUS_QUEUED}

class RequestModel(BaseModel):
    task_type: str = TASK_TYPE_DEMO_SLEEP_ECHO
    payload: dict

class ResponseModel(BaseModel):
    job_id: UUID
    status: str 
    task_type: str 
    payload: dict


@router.post("/jobs", response_model = ResponseModel)
def create_job(request: RequestModel):
    new_job = ResponseModel(
        job_id = uuid4(), 
        status = JOB_STATUS_QUEUED,
        task_type = request.task_type,
        payload = request.payload
        )

    jobs_store[str(new_job.job_id)] = new_job

    return new_job

@router.get("/jobs/{job_id}")
def retrieve_job(job_id: UUID):
    job = jobs_store.get(str(job_id))
    if job is None:
        raise HTTPException(status_code = 404, detail = "Job not found")
    return job

@router.get("/jobs", response_model = list[ResponseModel])
def retrieve_all_jobs():
    return jobs_store.values()