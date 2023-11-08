"""process-image function according to the MVC pattern."""
from src.api.models.process_image import ProcessImageRequest, ProcessImageResponse
from src.api.services.process_chunk import process_chunk
from src.db.processed_manager import ProcessedManager
from src.models.find_tags import FindTags
from src.models.ocr.ocr_interface import OCR
from src.utils.utils import get_abspath


async def process_image_service(
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
    data = ProcessedManager.get_data_by_id(req.uid)

    edited_paths = get_abspath("LOCAL_DATA", str(data.chunk_id), "edited")
    origin_paths = get_abspath("LOCAL_DATA", str(data.chunk_id), "original") 

    res = (await process_chunk(
        ocr_model=ocr_model,
        tags_model=tags_model,
        origin_paths=origin_paths,
        edited_path=edited_paths,
        image_names=[data.old_filename],
        chunk_id=data.chunk_id,
        rotate_angle=req.angle_to_rotate
    ))[0]

    response = ProcessImageResponse(
        uid=res.uid,
        old_filename=res.old_filename,
        duplicate_id=res.duplicate_id
    )

    return response
