from sqlalchemy import create_engine
from sqlalchemy.orm import Session, declarative_base

from app.core.config import settings

engine = create_engine(
    settings.SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

base = declarative_base()


def get_db():
    db = Session(bind=engine)

    try:
        yield db
    finally:
        db.close()