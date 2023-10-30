"""Checking file existing."""
import Levenshtein

from src.db.processed_manager import ProcessedManager, ProcessedStructure


def find_nearest_text(text1: str):
    """ Finding nearest document in database."""

    datas = ProcessedManager.get_all_data()

    nearest_uid = 0
    nearest_text = None
    nearest_distance = float('inf')

    # find min data with minimal distance
    for data in datas:
        # get all data
        data = ProcessedStructure().from_db(data)

        # determine the Levenshtein distance
        text2 = " ".join(data.text)
        distance = Levenshtein.distance(text1, text2)

        if distance < nearest_distance:
            nearest_uid = data.uid
            nearest_text = text2
            nearest_distance = distance

    return nearest_uid, nearest_text, nearest_distance


def find_duplicate_service(text: str, thresh: float = 0.5) -> int:
    """Checking file has processed.

    :param text: input text
    :param thresh: threshold value
    :return: UID of nearest text or -1 if it has cut by threshold value
    """
    if len(text) == 0:
        return -1

    nearest_uid, nearest_text, nearest_distance = find_nearest_text(text)
    if nearest_text is not None:
        similarity = nearest_distance / len(text)
        if similarity < thresh:
            return nearest_uid

    return -1
