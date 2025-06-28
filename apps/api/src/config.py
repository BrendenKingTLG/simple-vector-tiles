"""Configuration and constants for the tile server."""

import os

from openmaptiles.tileset import Tileset

# Database connection string
DATABASE_URL = os.getenv(
    "DATABASE_URL", "postgresql://openmaptiles:openmaptiles@localhost:5432/openmaptiles"
)

# Path to OpenMapTiles tileset definition
STYLE_DIR = "/app/style"
FONT_DIR = "/app/fonts"

# Load tileset once at startup
tileset = Tileset.parse(f"/app/openmaptiles.yaml")
