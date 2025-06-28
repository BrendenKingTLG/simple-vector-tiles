"""Entry point for the FastAPI tile service application."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src import db
from src.routers import static, tiles

app = FastAPI(title="Vector Tile API", version="1.0.0")

# Enable CORS for all origins (adjust in production if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register startup/shutdown events
app.add_event_handler("startup", db.connect_db)
app.add_event_handler("shutdown", db.disconnect_db)

# Include routers
app.include_router(tiles.router)
app.include_router(static.router)
