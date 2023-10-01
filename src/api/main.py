""" FastAPI connection """
from typing import List
from fastapi import FastAPI, UploadFile, Form, File
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
    results: dict[str, Result]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    ids: List[int]
    images: List[UploadFile]


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(ids: List[str] = Form(...), images: List[UploadFile] = File(...)):
    """ Process image function """
    images = [await image.read() for image in images]
    ids = [j for i in ids for j in i.split(',')]

    print(type(ids), type(ids[0]), print(ids))
    assert len(images) == len(ids), \
        f"Length of ids: {len(ids)} and images: {len(images)} should be equal."

    # convert to numpy arrays
    images = [pp.byte2numpy(image) for image in images]

    # use model
    outputs = model(images)

    response = OCRResponse(results={})
    for i, output in enumerate(outputs):
        response.results[ids[i]] = Result(
            tags=["None"],
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )

    return response


@app.get("/", response_class=HTMLResponse)
async def root():
    """ Init website """
    return '''
    
    '''


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
