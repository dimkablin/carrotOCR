"""process-image function according to the MVC pattern."""
import os.path

from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse, Result
from src.db.processed_manager import ProcessedManager, ProcessedStructure
import src.features.build_features as pp
from src.models.ocr.ocr import OCRModelFactoryProcessor
from src.utils.utils import get_abspath


def get_path_to_image(filename) -> str:
    """Getting path to the file located in LOCAL_DATA"""
    return os.path.join(get_abspath("LOCAL_DATA"), filename)


async def process_image_service(model: OCRModelFactoryProcessor, req: ProcessImageRequest):
    """ Controller for process image. """
    response = ProcessImageResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    # read images and use model
    images = await pp.read_images(req.paths)
    images = await pp.preprocess_images(images)
    outputs = model(images)

    for i, output in enumerate(outputs):
        # Find the duplicate
        duplicate_id = -1

        # insert data to Database and get UID
        data = ProcessedStructure(
            path=req.paths[i],
            old_filename=os.path.split(req.paths[i])[-1],
            tags=["None"],
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )
        uid = ProcessedManager.insert_data(data)

        # fill response
        response.results.append(Result(uid=uid, duplicate_id=duplicate_id))

    return response
