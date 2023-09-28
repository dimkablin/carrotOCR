""" FastAPI connection """
from typing import List

from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel
from src.models.ocr import OCRModelFactory

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    image: File
    text: List[str]
    bboxes: List[tuple[int]]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    images: List[UploadFile]


@app.post("/process-image/", response_model=List[OCRResponse])
async def process_image(req: OCRRequest):
    """ Process image function """
    images = [await img.read() for img in req.images]
    outputs = model(images)

    return [{
        'image': None,
        'text': output['rec_texts'],
        'bboxes': output['det_polygons']
    } for output in outputs]


@app.get("/")
async def root():
    """ Init message """
    return {"message": "Hello, World!"}
