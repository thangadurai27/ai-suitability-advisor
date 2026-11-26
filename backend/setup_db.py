"""Compatibility wrapper: create tables and seed data with SQLAlchemy models.

The old hand-written sqlite3 script created a schema that did not match the
ORM models. Use this script (or ``python seed.py``) instead.
"""

from app.database import Base, engine
from app.seed import create_seed_data


def setup_database() -> None:
    Base.metadata.create_all(bind=engine)
    create_seed_data()


if __name__ == "__main__":
    setup_database()
    print("Database setup complete.")
