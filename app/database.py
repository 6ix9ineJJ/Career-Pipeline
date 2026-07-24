from collections.abc import Generator
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

# SQLite stores the project data in one local file.
# This is perfect for a beginner CRUD project because no separate database server is needed.
DATABASE_PATH = Path(__file__).resolve().parent.parent / "career_pipeline.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"

# The engine is SQLAlchemy's connection point to the database.
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

# A session is used inside each API request to read/write database rows.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    # All SQLAlchemy models will inherit from this base class.
    pass


def get_db() -> Generator[Session, None, None]:
    # FastAPI dependency: open a database session for one request, then close it.
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
