from fastapi import FastAPI
from app.api.routes.jobs import router
from app.core.config import settings

#creating the fastapi app object
app = FastAPI(title = settings.APP_NAME)

#including the routing object to attach endpoints from the jobs router into the app
app.include_router(router)