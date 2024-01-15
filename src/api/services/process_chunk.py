# pylint: disable=R
"""process-image function according to the MVC pattern."""

import os
import time
import logging
from typing import List
from fastapi import WebSocket
import cv2

from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse, ProgressResponse
from src.api.models.process_image import ProcessImageResponse
from src.api.routers.utils import send_progress_sync
from src.api.services.process_image import process_image
from src.db.processed_manager import ProcessedManager
from src.env import DATA_PATH
import src.features.extract_features as pp
from src.models.ocr_models.ocr_interface import OCR
from src.utils.utils import create_dir_if_not_exist
from src.models.find_tags import FindTags

def process_chunk_service(
        ocr_model: OCR,
        tags_model: FindTags,
        req: ProcessChunkRequest,
        connections: List[WebSocket] = None) -> ProcessChunkResponse:
    """ process a chunk of data. 

    Args:
        ocr_model (OCRModelFactoryProcessor): OCR model class
        tags_model (FindTags): FindTags model that will find model
        req (ProcessChunkRequest): request from frontend
        
    Returns:
        ProcessChunkResponse: response of process chunk
    """
    start_time = time.time()
    paths = os.path.join(DATA_PATH, str(req.chunk_id))
    image_names = [i.split("/")[-1] for i in os.listdir(paths)]
    create_dir_if_not_exist(paths)
    response = ProcessChunkResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    # read images and use model
    paths_to_images = [paths+"/"+i for i in image_names]
    images = pp.read_images(paths_to_images)
    logging.info(
        "Read %d images in %.3f seconds",
        len(image_names),
        time.time() - start_time
    )
    start_time = time.time()

    # Prepare images
    images = pp.pipeline_images(images, connections=connections)

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

        # senf progress bar
        if connections is not None:
            for connection in connections:
                send_progress_sync(
                    connection,
                    ProgressResponse(
                        iter=i + len(images),
                        length=2 * len(images),
                        message="Обработка моделью."
                    )
                )

    # delete images from GPU or CPU
    del images

    logging.info(
        "Processed %d images with %s model in %.3f seconds.",
        len(image_names),
        ocr_model.get_model_type(),
        time.time() - start_time
    )
    return response
