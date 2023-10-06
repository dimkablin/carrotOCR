""" FastAPI connection """
from fastapi import FastAPI

from src.api.controllers.process_image import process_image_controller
from src.api.models.ocr_request import OCRRequest
from src.api.models.ocr_response import OCRResponse


app = FastAPI()


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(req: OCRRequest):
    """ Process image function """
    return await process_image_controller(req)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)  # 127.0.0.1:8000/api/..
