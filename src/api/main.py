""" FastAPI connection """
from typing import List

from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from src.models.ocr import OCRModelFactory

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    image: str
    text: List[str]
    bboxes: List[List[int]]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    image: UploadFile


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(req: OCRRequest):
    """ Process image function """
    image = await req.image.read()
    outputs = model([image])

    return [{
        'image': None,
        'text': output['rec_texts'],
        'bboxes': output['det_polygons']
    } for output in outputs]


@app.get("/", response_class=HTMLResponse)
async def root():
    """ Init website """
    return '''
    <html>
    <head>
        <title>OCR Image Processing</title>
    </head>
    <body>
        <h1>OCR Image Processing Service</h1>
        <form action="/process-image/" method="post" enctype="multipart/form-data">
            <input type="file" name="image" accept="image/*">
            <input type="submit" value="Process Image">
        </form>
    </body>
    </html>
    '''

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
