"""Cloud database notes/adapter boundary.
The executable backend uses SQLAlchemy so SQLite and PostgreSQL can share models.
Configure DATABASE_URL for Supabase/PostgreSQL in cloud mode.
"""
from sqlalchemy import create_engine

def create_database_engine(database_url: str):
    return create_engine(database_url, pool_pre_ping=True)
