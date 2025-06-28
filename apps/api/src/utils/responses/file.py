"""Utility functions for serving files and handling errors."""

import os

from fastapi import HTTPException
from fastapi.responses import FileResponse


def file_response_or_404(path: str, media_type: str) -> FileResponse:
    """
    Return a FileResponse if the file exists, otherwise raise 404.

    Args:
        path (str): Full path to the file.
        media_type (str): MIME type to serve the file with.

    Returns:
        FileResponse: FastAPI file response.
    """
    if not os.path.exists(path):
        raise HTTPException(
            status_code=404, detail=f"{os.path.basename(path)} not found")
    return FileResponse(path, media_type=media_type)
