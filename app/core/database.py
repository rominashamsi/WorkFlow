from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base 
from app.core.config import settings


engine=create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})

base=declarative_base()
