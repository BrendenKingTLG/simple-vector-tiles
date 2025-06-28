"""Route for serving on-demand Mapbox vector tiles."""

import traceback

from fastapi import APIRouter, HTTPException, Response
from openmaptiles.sqltomvt import MvtGenerator
from src import config, db

router = APIRouter()


@router.get("/tiles/{z}/{x}/{y}.pbf")
async def get_tile(z: int, x: int, y: int):
    """
    Generate a vector tile for the specified tile coordinates from PostGIS.

    Args:
        z (int): Zoom level.
        x (int): X coordinate of the tile.
        y (int): Y coordinate of the tile.

    Returns:
        Response: Protobuf tile data or HTTP error.
    """
    try:
        async with db.db_pool.acquire() as conn:
            postgis_ver = await conn.fetchval("SELECT PostGIS_Full_Version()")
            gen = MvtGenerator(tileset=config.tileset,
                               postgis_ver=postgis_ver, zoom=z, x=x, y=y)
            sql = gen.generate_sql()
            tile = await conn.fetchval(sql)

    except Exception as e:
        traceback.print_exc()
        raise HTTPException(
            status_code=500, detail=f"Tile generation error: {e}")

    if tile:
        return Response(tile, media_type="application/x-protobuf")
    raise HTTPException(status_code=204, detail="No tile data")
