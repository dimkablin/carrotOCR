""" FastAPI connection """
from typing import List
from fastapi import FastAPI, UploadFile
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


class Result(BaseModel):
    """ OCR model result type """
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    results: dict[int, Result]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    ids: List[int]
    images: List[UploadFile]


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(req: OCRRequest):
    """ Process image function """
    images = [await image.read() for image in req.images]

    # convert to numpy arrays
    images = [pp.byte2numpy(image) for image in images]

    # use model
    outputs = model(images)

    response = OCRResponse()
    for i, output in outputs:
        response.results[req.ids[i]] = Result(
            tags=["None"],
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )

    return response


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
            <label for="ids">Image IDs (comma-separated):</label>
            <input type="text" id="ids" name="ids">
            <br>
            <label for="images">Choose image files:</label>
            <input type="file" id="images" name="images" multiple accept="image/*">
            <br>
            <input type="submit" value="Process Images">
        </form>
    </body>
    </html>
    '''


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='192.168.31.127', port=8000)
