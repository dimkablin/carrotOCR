"""get_chunk_id_service function service."""


import os
from src.utils.utils import get_abspath


def create_chunk_id_dir(dirname: str) -> None:
    """create_chunk_id_dir function service."""
    if not os.path.exists(get_abspath("LOCAL_DATA", dirname)):
        os.mkdir(get_abspath("LOCAL_DATA", dirname))


async def get_chunk_id_service() -> int:
    """Get the next chunk ID."""
    # Получение списка каталогов и фильтрация только числовых
    local_data_path = get_abspath("LOCAL_DATA")
    numeric_dirs = [dir_ for dir_ in os.listdir(local_data_path)
                    if dir_.isdigit() and os.path.isdir(os.path.join(local_data_path, dir_))]

    # Сортировка числовых каталогов и получение следующего ID
    if numeric_dirs:
        next_uid = max(map(int, numeric_dirs)) + 1
    else:
        next_uid = 1

    # Создание каталога для нового chunk ID
    create_chunk_id_dir(str(next_uid))
    return next_uid
