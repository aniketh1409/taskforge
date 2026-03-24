from pydantic import BaseModel
from app.core.constants import (TASK_TYPE_DEMO_SLEEP_ECHO)
from uuid import UUID


class RequestModel(BaseModel):
    task_type: str = TASK_TYPE_DEMO_SLEEP_ECHO
    payload: dict

class ResponseModel(BaseModel):
    job_id: UUID
    status: str 
    task_type: str 
    payload: dict
    result: dict | None = None
    error: str | None = None
