"""process-image function according to the MVC pattern."""
import os.path

from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse, Result
from src.db.processed_manager import ProcessedManager, ProcessedStructure
import src.features.build_features as pp
from src.models.ocr.ocr import OCRModelFactoryProcessor
from src.utils.utils import get_abspath, read_paths, save_images
from src.models.find_tags import FindTags

async def process_image_service(
        ocr_model: OCRModelFactoryProcessor,
        tags_model: FindTags,
        req: ProcessImageRequest):
    """ Controller for process image. """

    response = ProcessImageResponse(
        chunk_id=req.chunk_id,
        results=[]
    )
    paths = read_paths(get_abspath("LOCAL_DATA", str(req.chunk_id), "original"))

    # read images and use model
    images = await pp.pipeline_async(paths)

    # save images
    save_images(images=images, 
                image_names=[i.split("/")[-1] for i in paths],
                path=get_abspath("LOCAL_DATA", str(req.chunk_id), "edited"))

    # use model
    outputs = ocr_model(images)

    for i, output in enumerate(outputs):
        # Find the duplicate
        duplicate_id = -1

        # insert data to Database and get UID
        data = ProcessedStructure(
            chunk_id=req.chunk_id,
            old_filename=os.path.split(paths[i])[-1],
            tags=tags_model(n_out=10, texts=output['rec_texts']),
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )
        uid = ProcessedManager.insert_data(data)

        # fill response
        response.results.append(Result(
            uid=uid,
            old_filename=data.old_filename,
            duplicate_id=duplicate_id))

    return response
