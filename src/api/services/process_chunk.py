"""process-image function according to the MVC pattern."""
from typing import List
from src.api.models.process_chunk import ProcessChunkRequest, ProcessChunkResponse
from src.api.models.process_image import ProcessImageResponse
from src.db.processed_manager import ProcessedManager, ProcessedStructure
import src.features.build_features as pp
from src.models.ocr.ocr_interface import OCR
from src.utils.utils import get_abspath, read_paths, save_images
from src.models.find_tags import FindTags


async def process_chunk(
        ocr_model: OCR,
        tags_model: FindTags,
        origin_paths: str,
        edited_path: str,
        image_names: List[str], 
        chunk_id: int,
        rotate_angle=0) -> List[ProcessImageResponse]:
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

    # read images and use model
    paths_to_images = [origin_paths+"/"+i for i in image_names]
    images = await pp.read_images(paths_to_images)
    images = await pp.pipeline_async(images)

    # save images
    save_images(images, image_names, edited_path)

    # use model
    outputs = ocr_model(images)

    result = []
    for i, output in enumerate(outputs):
        # Find the duplicate
        duplicate_id = -1

        # insert data to Database and get UID
        data = ProcessedStructure(
            chunk_id=chunk_id,
            old_filename=image_names[i],
            tags=tags_model(n_out=10, texts=output['rec_texts']),
            text=output['rec_texts'],
            bboxes=output['det_polygons']
        )
        uid = ProcessedManager.insert_data(data)

        # fill response
        result.append(ProcessImageResponse(
            uid=uid,
            old_filename=data.old_filename,
            duplicate_id=duplicate_id)
        )

    return result


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

    edited_paths = get_abspath("LOCAL_DATA", str(req.chunk_id), "edited")
    origin_paths = get_abspath("LOCAL_DATA", str(req.chunk_id), "original")
    image_names = [i.split("/")[-1] for i in read_paths(origin_paths)]

    response = ProcessChunkResponse(
        chunk_id=req.chunk_id,
        results=[]
    )

    response.results = await process_chunk(
        ocr_model=ocr_model,
        tags_model=tags_model,
        origin_paths=origin_paths,
        edited_path=edited_paths,
        image_names=image_names,
        chunk_id=req.chunk_id
    )

    return response
