from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Single database location
DATABASE_PATH = BASE_DIR / "ledgerlens.db"


DATABASE_URL = f"sqlite:///{DATABASE_PATH}"


print("DATABASE URL:", DATABASE_URL)
print("DATABASE FILE:", DATABASE_PATH)


engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },
)


SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


Base = declarative_base()


def get_db():

    db = SessionLocal()

    try:
        yield db

    finally:
        db.close()