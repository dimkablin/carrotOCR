""" FastAPI connection """
import io
from typing import List

from PIL import Image
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    text: List[str]
    bboxes: List[List[int]]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    image: UploadFile


@app.post("/process-image/", response_model=List[OCRResponse])
async def process_image(image: UploadFile):
    """ Process image function """
    image = await image.read()

    # preprocess
    image = io.BytesIO(image)
    image = Image.open(image)
    image = pp.pil_to_numpy(image)

    outputs = model([image])

    return [OCRResponse(
        text=output['rec_texts'],
        bboxes=output['det_polygons']
    ) for output in outputs]


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

    uvicorn.run(app, host='192.168.31.127', port=8000)
