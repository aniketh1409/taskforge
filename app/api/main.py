from fastapi import FastAPI
from app.api.routes.jobs import router
from app.core.config import settings
from app.db.session import Base, engine
import app.db.models

#creating the fastapi app object
app = FastAPI(title = settings.APP_NAME)

#including the routing object to attach endpoints from the jobs router into the app
app.include_router(router)

#only creates those tables that sqlalchemy knows about, will only know if model module is imported
Base.metadata.create_all(bind = engine)

