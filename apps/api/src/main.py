import os
import traceback
import asyncio
import gzip
from fastapi import FastAPI, HTTPException, Response
import asyncpg
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from urllib.parse import unquote
from openmaptiles.tileset import Tileset
from openmaptiles.sqltomvt import MvtGenerator
import asyncpg

tileset = Tileset.parse('openmaptiles.yaml')

DATABASE_URL = os.getenv("DATABASE_URL","postgresql://openmaptiles:openmaptiles@localhost:5432/openmaptiles")
LAYERS_DIR = "layers"
PIXEL_WIDTH = 0.28
LAYERS_WITH_PIXEL_WIDTH = {"place", "poi", "city", "park", "mountain_peak"}

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.on_event("startup")
async def startup():
    app.state.db_pool = await asyncpg.create_pool(DATABASE_URL)

@app.on_event("shutdown")
async def shutdown():
    await app.state.db_pool.close()

@app.get("/sprite.json")
async def get_sprite():
    path = os.path.join("style", "sprite.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sprite.json not found")
    return FileResponse(path, media_type="application/json")

@app.get("/sprite@2x.json")
async def get_sprite_png():
    path = os.path.join("style", "sprite@2x.json")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sprite.png not found")
    return FileResponse(path, media_type="image/png")

@app.get("/sprite@2x.png")
async def get_sprite2_png():
    path = os.path.join("style", "sprite@2x.png")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sprite.png not found")
    return FileResponse(path, media_type="image/png")

@app.get("/sprite.png")
async def get_sprit2e_png():
    path = os.path.join("style", "sprite.png")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="sprite.png not found")
    return FileResponse(path, media_type="image/png")

@app.get("/fonts/{fontstack:path}/{range}.pbf")
async def get_font(fontstack: str, range: str):
    font_dir = "fonts"
    decoded_fonts = [unquote(f.strip()) for f in fontstack.split(",")]
    for font in decoded_fonts:
        path = os.path.join(font_dir, font, f"{range}.pbf")
        if os.path.isfile(path):
            return FileResponse(path, media_type="application/x-protobuf")
    raise HTTPException(status_code=404, detail="Font not found")

@app.get("/style.json")
async def get_style():
    return FileResponse("style/style-header.json", media_type="application/json")

@app.get("/openmaptiles.json")
async def get_open():
    return FileResponse("openmaptiles.json", media_type="application/json")

@app.get("/tiles/{z}/{x}/{y}.pbf")
async def get_tile(z: int, x: int, y: int):
    conn = await asyncpg.connect(DATABASE_URL)
    postgis_ver = await conn.fetchval("SELECT PostGIS_Full_Version()")

    gen = MvtGenerator(
        tileset=tileset,
        postgis_ver=postgis_ver,
        zoom=z,
        x=x,
        y=y
    )

    sql = gen.generate_sql()
    try:
        tile = await conn.fetchval(sql)
        await conn.close()
    except Exception as e:
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Tile gen error: {e}")

    if tile:
        return Response(tile, media_type="application/x-protobuf")
    else:
        raise HTTPException(status_code=204, detail="No tile data")
