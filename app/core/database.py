from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, Session

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