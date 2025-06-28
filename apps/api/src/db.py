"""Database pool connection manager."""

import asyncpg
from src.config import DATABASE_URL

db_pool = None


async def connect_db():
    """
    Create a global connection pool to the PostgreSQL database.
    This pool is reused for all tile queries.
    """
    global db_pool
    db_pool = await asyncpg.create_pool(DATABASE_URL)


async def disconnect_db():
    """
    Close the global connection pool on application shutdown.
    """
    await db_pool.close()
