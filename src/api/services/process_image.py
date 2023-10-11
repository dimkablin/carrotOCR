"""process-image function according to the MVC pattern."""
from src.api.models.process_image_models import ProcessImageRequest, ProcessImageResponse, Result
from src.db.database_processor import DataProcessor
from src.models.ocr import OCRModelFactory
import src.features.build_features as pp

model = OCRModelFactory.create("pytesseract")


async def process_image_controller(req: ProcessImageRequest):
    """ Controller for process image. """
    response = ProcessImageResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    try:
        # read images and use model
        images = await pp.read_images(req.paths)
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

            # fill response
            response.results.append(Result(uid=uid, **data))

    except FileNotFoundError as err:
        print(err)

    return response
