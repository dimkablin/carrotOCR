# pylint: disable=R
"""process-image function according to the MVC pattern."""
import time
import logging

from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.models.process_image import ProcessImageResponse
from src.api.services.process_image import process_image
from src.db.processed_manager import ProcessedManager
import src.features.extract_features as pp
from src.models.ocr.ocr_interface import OCR
from src.utils.utils import create_dir_if_not_exist, get_abspath, read_paths
from src.models.find_tags import FindTags



def process_chunk_service(
        ocr_model: OCR,
        tags_model: FindTags,
        req: ProcessChunkRequest) -> ProcessChunkResponse:
    """ process a chunk of data. 

    Args:
        ocr_model (OCRModelFactoryProcessor): _description_
        tags_model (FindTags): _description_
        req (ProcessChunkRequest): _description_
        
    Returns:
        ProcessChunkResponse: response of process chunk
    """
    start_time = time.time()

    origin_paths = get_abspath("LOCAL_DATA", str(req.chunk_id), "original")
    image_names = [i.split("/")[-1] for i in read_paths(origin_paths)]

    edited_paths = get_abspath("LOCAL_DATA", str(req.chunk_id), "edited")
    create_dir_if_not_exist(edited_paths)
    edited_paths = [edited_paths+"/"+image_name for image_name in image_names]

    response = ProcessChunkResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    # read images and use model
    paths_to_images = [origin_paths+"/"+i for i in image_names]
    images = pp.read_images(paths_to_images)
    images = pp.pipeline_images(images, edited_paths)

    logging.info(
        "Pipeline executed %d images in %.3f seconds",
        len(image_names),
        time.time() - start_time
    )
    start_time = time.time()
    for i, image in enumerate(images):
        data = process_image(
            image=image,
            ocr_model=ocr_model,
            tags_model=tags_model,
            image_name=image_names[i],
            chunk_id=req.chunk_id
        )

        data.angle = 0
        uid = ProcessedManager.insert_data(data)

        response.results.append(
            ProcessImageResponse(
                uid=uid,
                old_filename=data.old_filename,
                duplicate_id=-1
            )
        )

    logging.info(
        "Processed %d images with %s model in %.3f seconds.",
        len(image_names),
        ocr_model.get_model_type(),
        time.time() - start_time
    )
    return response
