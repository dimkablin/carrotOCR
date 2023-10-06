""" FastAPI connection """
from typing import List

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from src.db.database_processor import DataProcessor
from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

# Init app
app = FastAPI()
model = OCRModelFactory.create("pytesseract")


class Result(BaseModel):
    """ OCR model result type """
    uid: int  # Image ID
    file_path: str
    tags: List[str]
    text: List[str]
    bboxes: List[List[int]]


# create structures
class OCRResponse(BaseModel):
    """ Response of the OCR model """
    chunk_id: int  # Chunk ID
    results: List[Result]


class OCRRequest(BaseModel):
    """ Request to the OCR model """
    chunk_id: int  # Chunk ID
    paths: List[str]


@app.post("/process-image/", response_model=OCRResponse)
async def process_image(req: OCRRequest):
    """ Process image function """
    response = OCRResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    try:
        images = await pp.read_images(req.paths)

        # use model
        outputs = model(images)

        for i, output in enumerate(outputs):
            data = {
                "file_path": req.paths[i],
                "tags": ["None"],
                "text": output['rec_texts'],
                "bboxes": output['det_polygons']
            }

            uid = DataProcessor.insert_data(**data)
            response.results.append(Result(
                uid=uid,
                **data
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
