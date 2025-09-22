#backend\database\database.py
import threading
from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
from backend.models import Base
from backend.utils.env import DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD

load_dotenv()  # Load environment variables from .env file

class DatabaseConnection:
    _engine = None
    _SessionLocal = None
    _instance = None
    _lock = threading.Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._engine = create_engine(
                        f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
                    )
                    cls._instance._SessionLocal = sessionmaker(bind=cls._instance._engine)
                    Base.metadata.create_all(cls._instance._engine)
        return cls._instance

    def get_session(self) -> Session:
        return self._SessionLocal()

# Create a singleton instance
_db_instance = DatabaseConnection()

# Provide a simple function to get session for convenience
def get_session() -> Session:
    return _db_instance.get_session()

# Use this with FastAPI Depends (and tests that expect a generator)
def get_db():
    db = get_session()
    try:
        yield db
    finally:
        db.close()
