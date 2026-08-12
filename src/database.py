"""
Database connection utilities for Project VIGIL.
"""

import os
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_db_connection() -> Engine:
    """
    Create and return a SQLAlchemy database engine.

    Returns:
        Engine: SQLAlchemy engine connected to Neon PostgreSQL.
    """
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL not found in .env file")

    engine = create_engine(database_url)
    return engine


def test_connection():
    """
    Test the database connection by running a simple query.
    """
    engine = get_db_connection()
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ Database connection successful!")
        print(f"   Query result: {result.fetchone()[0]}")


if __name__ == "__main__":
    test_connection()