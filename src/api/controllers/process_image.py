"""/process-image/ function according to the MVC pattern."""
from src.api.models.ocr_request import OCRRequest
from src.api.models.ocr_response import OCRResponse
from src.api.models.result import Result
from src.db.database_processor import DataProcessor
from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

model = OCRModelFactory.create("pytesseract")


async def process_image_controller(req: OCRRequest):
    """ Controller for process image. """
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

            # insert data to Database and get UID
            uid = DataProcessor.insert_data(**data)

            # fill response model
            response.results.append(Result(uid=uid, **data))

    except FileNotFoundError as err:
        print(err)

    return response
