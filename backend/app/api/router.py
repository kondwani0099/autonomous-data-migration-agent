"""Central API Router aggregation."""

from fastapi import APIRouter
from app.api.jobs import router as jobs_router
from app.api.upload import router as upload_router
from app.api.clarifications import router as clarifications_router
from app.api.preview import router as preview_router
from app.api.clients import router as clients_router
from app.api.categories import router as categories_router

api_router = APIRouter()

api_router.include_router(jobs_router, prefix="/jobs", tags=["Jobs"])
api_router.include_router(upload_router, prefix="/jobs", tags=["Upload"])
api_router.include_router(clarifications_router, prefix="/jobs", tags=["Clarifications"])
api_router.include_router(preview_router, prefix="/jobs", tags=["Preview & Import"])
api_router.include_router(clients_router, prefix="/clients", tags=["Clients"])
api_router.include_router(categories_router, tags=["Data Categories"])
