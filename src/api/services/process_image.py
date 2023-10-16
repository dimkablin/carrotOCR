"""process-image function according to the MVC pattern."""
from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse, Result
from src.db.database_processor import DataProcessor
from src.models.ocr.ocr import OCRModelFactoryProcessor
import src.features.build_features as pp


MODEL = OCRModelFactoryProcessor("pytesseract")


async def process_image_service(req: ProcessImageRequest):
    """ Controller for process image. """
    response = ProcessImageResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    # read images and use model
    images = await pp.read_images(req.paths)
    outputs = MODEL(images)

    for i, output in enumerate(outputs):
        data = {
            "file_path": req.paths[i],
            "tags": ["None"],
            "text": output['rec_texts'],
            "bboxes": output['det_polygons']
        }

        # insert data to Database and get UID
        uid = DataProcessor.insert_data(**data)

        # fill response
        response.results.append(Result(uid=uid, **data))

    return response
