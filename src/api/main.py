""" FastAPI connection """
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware

from src.api.controllers.get_files import get_files_controller
from src.api.controllers.get_folders import get_folders_controller
from src.api.controllers.process_image import process_image_controller
from src.api.models.get_f_models import GetFRequest, GetFResponse
from src.api.models.process_image_models import ProcessImageRequest, ProcessImageResponse

app = FastAPI()
router = APIRouter()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@router.post("/process-image/", response_model=ProcessImageResponse)
async def process_image(req: ProcessImageRequest):
    """ Process image function """
    return await process_image_controller(req)


@router.post("/get-files/", response_model=GetFResponse)
async def get_files(req: GetFRequest):
    """Returning all directories in path."""
    return await get_files_controller(req)


@router.post("/get-folders/", response_model=GetFResponse)
async def get_folders(req: GetFRequest):
    """Returning all directories in path."""
    return await get_folders_controller(req)

app.include_router(router, prefix="/api")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)  # 127.0.0.1:8000/api/..
