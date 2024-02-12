""" FastAPI connection """
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from src.api.middleware.middleware import BackendMiddleware
from src.env import DATA_PATH

from src.utils.utils import create_dir

from src.api.endpoints import ai_models, data, database, websocket

# LOGGING CONFIG SETTING
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logging.info("Running server.")

create_dir(DATA_PATH)

app = FastAPI(
    title="Backend API",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json",
    openapi_tags=[{
        "name": "Backend API",
        "description": "Backend API router."
    }]
)

app.add_middleware(BackendMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
app.mount("/api/LOCAL_DATA", StaticFiles(directory=DATA_PATH), name="LOCAL_DATA")

app.include_router(ai_models.router, prefix="/api", tags=["ai_models"])
app.include_router(data.router, prefix="/api", tags=["data"])
app.include_router(database.router, prefix='/api', tags=["database"])
app.include_router(websocket.router, prefix='/api', tags=["websocket"])
