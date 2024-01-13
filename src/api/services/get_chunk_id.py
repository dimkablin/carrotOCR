"""get_chunk_id_service function service."""


import os
from src.env import DATA_PATH


def create_chunk_id_dir(dirname: str) -> None:
    """create_chunk_id_dir function service."""
    if not os.path.exists(os.path.join(DATA_PATH, dirname)):
        os.mkdir(os.path.join(DATA_PATH, dirname))


def get_chunk_id_service() -> int:
    """Get the next chunk ID."""
    # Получение списка каталогов и фильтрация только числовых
    numeric_dirs = [dir_ for dir_ in os.listdir(DATA_PATH)
                    if dir_.isdigit() and os.path.isdir(os.path.join(DATA_PATH, dir_))]

    # Сортировка числовых каталогов и получение следующего ID
    if numeric_dirs:
        next_uid = max(map(int, numeric_dirs)) + 1
    else:
        next_uid = 1

    # Создание каталога для нового chunk ID
    create_chunk_id_dir(str(next_uid))
    return next_uid
