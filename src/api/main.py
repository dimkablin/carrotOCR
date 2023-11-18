""" FastAPI connection """
import logging

from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.api.middleware.middleware import BackendMiddleware
from src.utils.utils import get_abspath
from src.api.routers.connection_manager import ConnectionManager
from src.api.routers.pipeline_router import pipeline_router
from src.api.routers.data_router import data_router
from src.api.routers.websocket import websoket_router
from src.api.routers.models_router import ml_model_router

connection_manager = ConnectionManager()

# LOGGING CONFIG SETTING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logging.info("Running server.")

app = FastAPI(
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=[{
        "name": "Backend API",
        "description": "Backend API router."
    }]
)
router = APIRouter()

app.add_middleware(BackendMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.mount("/api/LOCAL_DATA", StaticFiles(directory=get_abspath("LOCAL_DATA")), name="LOCAL_DATA")

app.include_router(router, prefix="/api")
app.include_router(pipeline_router, prefix="/api")
app.include_router(data_router, prefix='/api')
app.include_router(websoket_router, prefix='/api')
app.include_router(ml_model_router, prefix="/api")
