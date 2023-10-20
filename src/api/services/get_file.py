"""fet_file function service."""
import os.path
from pathlib import Path
from fastapi.responses import FileResponse


async def get_file_service(filename):
    """get file service's main function."""
    path = Path("LOCAL_DATA") / filename
    if os.path.exists(path):
        return FileResponse(path)
