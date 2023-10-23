"""process-image function according to the MVC pattern."""
from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse, Result
from src.db.processed_manager import ProcessedManager, ProcessedStructure
import src.features.build_features as pp
from src.models.ocr.ocr import OCRModelFactoryProcessor


async def process_image_service(model: OCRModelFactoryProcessor, req: ProcessImageRequest):
    """ Controller for process image. """
    response = ProcessImageResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    # read images and use model
    images = await pp.read_images(req.paths)
    outputs = model(images)

    for i, output in enumerate(outputs):
        data = ProcessedStructure(
            old_filename=req.paths[i],
            tags=["None"],
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )

        # insert data to Database and get UID
        uid = ProcessedManager.insert_data(data)

        # fill response
        response.results.append(Result(uid=uid, **data.to_db()))

    return response
