""" FastAPI connection """
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


class Result(BaseModel):
    """ OCR model result type """
    id: int  # Image ID
    path: str
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    id: int  # Chunk ID
    results: List[Result]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    id: int  # Chunk ID
    paths: List[str]


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(req: OCRRequest):
    """ Process image function """
    response = OCRResponse(
        id=req.id,
        results=[]
    )

    try:
        images = await pp.read_images(req.paths)

        # use model
        outputs = model(images)

        for i, output in enumerate(outputs):
            response.results.append(Result(
                id=i,
                path=req.paths[i],
                tags=["None"],
                text=output['rec_texts'],
                bboxes=output['det_polygons']
            ))

    except FileNotFoundError as err:
        print(err)

    return response


@app.get("/", response_class=HTMLResponse)
async def root():
    """ Init website """
    return ''' '''


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host='127.0.0.1', port=8000)
