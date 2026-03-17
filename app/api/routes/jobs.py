from fastapi import APIRouter
from app.core.constants import JOB_STATUS_SUCCEEDED, JOB_STATUS_RUNNING, JOB_STATUS_FAILED, JOB_STATUS_QUEUED, TASK_TYPE_DEMO_SLEEP_ECHO
from pydantic import BaseModel
from uuid import UUID, uuid4


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
    return ResponseModel(
        job_id = uuid4(), 
        status = JOB_STATUS_QUEUED,
        task_type = TASK_TYPE_DEMO_SLEEP_ECHO
        payload = request.payload
        )
        
    
