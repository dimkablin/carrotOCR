# pylint: disable=R
"""process-image function according to the MVC pattern."""
import time
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.services.process_image import process_image
import src.features.build_features as pp
from src.models.ocr.ocr_interface import OCR
from src.utils.utils import create_dir_if_not_exist, get_abspath, read_paths
from src.models.find_tags import FindTags
import logging


async def process_chunk_service(
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
    images = await pp.read_images(paths_to_images)
    images = await pp.pipeline_images(images, edited_paths)

    logging.debug(
        "Pipeline images executed in %s seconds", 
        str(time.time() - start_time)
    )
    start_time = time.time()

    for i, image in enumerate(images):
        response.results.append(process_image(
            image=image,
            ocr_model=ocr_model,
            tags_model=tags_model,
            image_name=image_names[i],
            chunk_id=req.chunk_id
        ))

    logging.debug(
        "Processed image with %s model in %s seconds.", 
        ocr_model.get_model_type(),
        str(time.time() - start_time)
    )
    return response
