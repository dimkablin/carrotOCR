"""get_chunk_id_service function service."""


import os
from src.utils.utils import get_abspath


def create_chunk_id_dir(dirname: str) -> None:
    """create_chunk_id_dir function service."""
    if not os.path.exists(get_abspath("LOCAL_DATA", dirname)):
        os.mkdir(get_abspath("LOCAL_DATA", dirname))


async def get_chunk_id_service() -> int:
    """get chunk id service's main function."""
    folders_in_local_data = []
    for dir_ in os.listdir(get_abspath("LOCAL_DATA")):
        if os.path.isdir(os.path.join(get_abspath("LOCAL_DATA"), dir_)):
            folders_in_local_data.append(dir_)

    uid = int(folders_in_local_data[-1]) + 1 if len(folders_in_local_data) != 0 else 1
    create_chunk_id_dir(str(uid))
    return uid
