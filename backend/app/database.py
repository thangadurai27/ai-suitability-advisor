"""Database module for AI Suitability Advisor.

Provides a single SQLAlchemy engine, session factory and the shared declarative
Base used by every model. PostgreSQL/Supabase can be selected with DATABASE_URL;
SQLite is the zero-setup development default.
"""

from __future__ import annotations

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Models define Base, so importing it here guarantees one metadata registry.
from .models import Base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ai_suitability_advisor.db")

_connect_args: dict = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    connect_args=_connect_args,
    echo=os.getenv("SQL_ECHO", "False").lower() == "true",
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db() -> Generator[Session, None, None]:
    """Yield a database session that is always closed."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    """Create all tables defined in app.models."""
    Base.metadata.create_all(bind=engine)


def drop_all_tables() -> None:
    """Drop all tables (testing/reset only)."""
    Base.metadata.drop_all(bind=engine)


__all__ = ["Base", "engine", "SessionLocal", "get_db", "init_db", "drop_all_tables", "DATABASE_URL"]
