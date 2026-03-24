from app.db.session import Base
from sqlalchemy import Column, String, JSON

class Job(Base):
    __tablename__ = "jobs"
    id = Column(String, nullable = False, primary_key= True, unique= True)
    status = Column(String)
    task_type = Column(String)
    payload = Column(JSON)
    result = Column(JSON)
    error = Column(String)