"""process-image function according to the MVC pattern."""
import os
import time
import logging

import numpy as np
from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse
from src.db.processed_manager import ProcessedManager
from src.db.structures.processed_structure import ProcessedStructure
from src.env import DATA_PATH
from src.models.find_tags import FindTags
from src.models.ocr_models.ocr_interface import OCR
import src.features.extract_features as pp


def process_image(
        image: np.ndarray,
        ocr_model: OCR,
        tags_model: FindTags,
        image_name: str,
        chunk_id: int) -> ProcessedStructure:
    """ Main function to process a chunk of data

    Args:
        ocr_model (OCRModelFactoryProcessor): ocr model 
        tags_model (FindTags): model to find tags
        origin_paths (list[str]): paths of original images LOCAL_DATA/chunk_id/original
        edited_path (str): path to save edited images LOCAL_DATA/chunk_id/edited
        image_names (list[str]): names of images
        chunk_id (int): chunk ID

    Returns:
        ProcessChunkResponse: response of process chunk
    """

    # use model
    output = ocr_model([image])[0]

    data = ProcessedStructure(
        chunk_id=chunk_id,
        old_filename=image_name,
        tags=tags_model(n_out=10, texts=output['rec_texts']),
        text=output['rec_texts'],
        bboxes=output['det_polygons']
    )

    return data


def process_image_service(
        ocr_model: OCR,
        tags_model: FindTags,
        req: ProcessImageRequest) -> ProcessImageResponse:
    """ process a image. 

    Args:
        ocr_model (OCRModelFactoryProcessor): _description_
        tags_model (FindTags): _description_
        req (ProcessImageRequest): _description_
    
    Returns:
        response (ProcessImageResponse): response of process image
    """
    start_time = time.time()

    # get data from database
    data = ProcessedManager.get_data_by_id(req.uid)

    # read images and run general_pipeline
    paths = os.path.join(DATA_PATH, str(data.chunk_id))
    print(os.path.join(paths,  data.old_filename))
    image = pp.read_image(os.path.join(paths,  data.old_filename))

    image = pp.pipeline_image(image, pipeline_params=req.pipeline_params)

    logging.info("Pipeline images executed in %.3s seconds", time.time() - start_time)
    start_time = time.time()

    # fill response
    data = process_image(
        image=image,
        ocr_model=ocr_model,
        tags_model=tags_model,
        image_name=data.old_filename,
        chunk_id=data.chunk_id
    )

    # Get an angle from the BD and add it to the req
    data.angle = req.pipeline_params.angle

    # поменять начальную точку ббоксов отнсоительно оригинальной фотографии
    for bbox in data.bboxes:
        for coord in range(0, 7, 2):
            bbox[coord] += req.pipeline_params.cut.x1
            bbox[coord + 1] += req.pipeline_params.cut.y1

    ProcessedManager.update_data_by_id(data, req.uid)

    logging.info(
        "Processed image with %s model in %.3f seconds.", 
        ocr_model.get_model_type(),
        time.time() - start_time
    )

    res = ProcessImageResponse(
        uid=req.uid,
        old_filename=data.old_filename,
        duplicate_id=-1
    )

    return res
