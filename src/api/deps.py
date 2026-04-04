# endpoints/deps.py
from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session
from src.database.config import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DbSession = Annotated[Session, Depends(get_db)]
