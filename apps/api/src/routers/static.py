"""Routes for serving static resources like sprites, styles, and fonts."""

import os
from urllib.parse import unquote

from fastapi import APIRouter, HTTPException
from src.config import FONT_DIR, STYLE_DIR
from src.utils.responses import file_response_or_404

router = APIRouter()


@router.get("/sprite.json")
async def sprite_json():
    """Serve the sprite JSON file."""
    return file_response_or_404(os.path.join(STYLE_DIR, "sprite.json"), "application/json")


@router.get("/sprite@2x.json")
async def sprite_2x_json():
    """Serve the high-DPI sprite JSON file."""
    return file_response_or_404(os.path.join(STYLE_DIR, "sprite@2x.json"), "application/json")


@router.get("/sprite.png")
@router.get("/sprite@2x.png")
async def sprite_png():
    """
    Serve PNG sprite files (normal and @2x).
    FastAPI handles routing based on request path.
    """
    filename = router.routes[-1].path.split("/")[-1]
    return file_response_or_404(os.path.join(STYLE_DIR, filename), "image/png")


@router.get("/fonts/{fontstack:path}/{range}.pbf")
async def get_font(fontstack: str, range: str):
    """
    Serve Mapbox-compatible font glyphs based on fontstack and range.

    Args:
        fontstack (str): Comma-separated list of font names.
        range (str): Range of glyphs (e.g. "0-255").

    Returns:
        FileResponse: Font glyph PBF file if found.
    """
    decoded_fonts = [unquote(f.strip()) for f in fontstack.split(",")]
    for font in decoded_fonts:
        path = os.path.join(FONT_DIR, font, f"{range}.pbf")
        if os.path.isfile(path):
            return file_response_or_404(path, "application/x-protobuf")
    raise HTTPException(status_code=404, detail="Font not found")


@router.get("/style.json")
async def get_style():
    """Serve the main style JSON file."""
    return file_response_or_404(os.path.join(STYLE_DIR, "style-header.json"), "application/json")


@router.get("/openmaptiles.json")
async def get_openmaptiles():
    """Serve the OpenMapTiles metadata definition JSON."""
    return file_response_or_404(os.path.join(STYLE_DIR, "openmaptiles.json"), "application/json")
