"""AI models module."""

import os
from typing import List
import time
import logging
import numpy as np

from websocket import WebSocket

from src.db.files_manager import FilesManager
# importing path to the folder
from src.env import DATA_PATH
from src.api.models.data import IMAGE_EXTENSIONS

# importing interfaces
from src.ai_models.ocr import OCRModelFactory
from src.ai_models.find_tags import FindTags
from src.ai_models.ocr_models.ocr_interface import OCR

# importing fast api models
from src.api.models.ai_models import *

# importing packages to work with DataBase
from src.db.processed_manager import ProcessedManager
from src.db.structures.processed_structure import ProcessedStructure

# work with images
import src.features.extract_features as pp
import src.features.build_features as bf


class AIModels:
    """AI models class."""
    @staticmethod
    def get_ocr_models() -> GetOCRModelsResponse:
        """Get OCR Models service function."""
        models = OCRModelFactory.get_models()
        return GetOCRModelsResponse(models=models, default=0)

    @staticmethod
    def _process_image(
            image: np.ndarray,
            ocr_model: OCR,
            tags_model: FindTags,
            image_name: str,
            chunk_id: int) -> ProcessedStructure:
        """ Main function to process a chunk of data

        Args:
            image: input image
            ocr_model (OCRModelFactoryProcessor): ocr model
            tags_model (FindTags): model to find tags
            image_name (list[str]): names of images
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

    @staticmethod
    def process_image(
            ocr_model: OCR,
            tags_model: FindTags,
            req: ProcessImageRequest) -> ProcessFileResponse:
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
        image = pp.read_image(os.path.join(paths, data.old_filename))
        image = pp.pipeline_image(image, pipeline_params=req.pipeline_params)

        logging.info("Pipeline images executed in %.3s sec", time.time() - start_time)
        start_time = time.time()

        # fill response
        data = AIModels._process_image(
            image=image,
            ocr_model=ocr_model,
            tags_model=tags_model,
            image_name=data.old_filename,
            chunk_id=data.chunk_id
        )

        # Get an angle from the BD and add it to the req
        data.angle = req.pipeline_params.angle

        # повернуть боксы относительно оригинальной фотки
        data.bboxes = bf.rotate_bboxes(data.bboxes, -data.angle, image.shape[:2])

        # поменять начальную точку боксов относительно оригинальной фотографии
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

        res = ProcessFileResponse(
            uid=req.uid,
            old_filename=data.old_filename,
            duplicate_id=-1
        )

        return res

    @staticmethod
    def process_chunk(
            ocr_model: OCR,
            tags_model: FindTags,
            req: ProcessChunkRequest,
            tqdm) -> ProcessChunkResponse:
        """
        process a chunk of data.
        :param ocr_model:
        :param tags_model:
        :param req:
        :param tqdm:
        :return:
        """
        # init tqdm and response
        tqdm.message = "Обработка моделью."
        response = ProcessChunkResponse(chunk_id=req.chunk_id, results=[])

        # START LOGGING
        start_time = time.time()

        # process IMAGES in chunk_id
        path = os.path.join(DATA_PATH, str(req.chunk_id))
        results = AIModels._process_chunk(ocr_model, tags_model, req, path, tqdm)
        response.results += results

        # process PDF in chunk_id
        all_pdf = FilesManager().get_data_by_chunk_id(req.chunk_id)
        print(all_pdf)

        # read images and use model

        # END LOGGING
        logging.info(
            "Processed %d images with %s model in %.3f seconds.",
            tqdm.length, ocr_model.get_model_type(), time.time() - start_time
        )
        return response

    @staticmethod
    def _process_chunk(
            ocr_model: OCR,
            tags_model: FindTags,
            req: ProcessChunkRequest,
            path: str,
            tqdm) -> List[ProcessFileResponse]:
        """
        Internal function to process the chunk of images
        :param ocr_model: OCR model type
        :param tags_model: FindTags model that will find model
        :param req: request model with details
        :param : Paths to images
        :return: ProcessChunkResponse
        """
        results = []

        image_names = []
        for i in os.listdir(path):
            if pp.check_extension(i, IMAGE_EXTENSIONS):
                image_names.append(i.split("/")[-1])

        paths = [path + "/" + i for i in image_names]

        images = pp.read_images(paths)
        images = [pp.pipeline_image(image) for image in images]

        for i, image in enumerate(images):
            data = AIModels._process_image(
                image=image,
                ocr_model=ocr_model,
                tags_model=tags_model,
                image_name=image_names[i],
                chunk_id=req.chunk_id
            )

            data.angle = 0
            uid = ProcessedManager.insert_data(data)

            results.append(
                ProcessFileResponse(uid=uid, old_filename=data.old_filename, duplicate_id=-1)
            )

            # senf progress bar
            tqdm.update()

        # delete images from DEVICE
        del images

        return results
