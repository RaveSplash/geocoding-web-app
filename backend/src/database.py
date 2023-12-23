from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Get the absolute path to the 'backend' directory
backend_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
# Specify the path for the SQLite database file in the 'backend' directory
database_path = os.path.join(backend_directory, "zuscoffee.db")

SQLALCHEMY_DATABASE_URL = f"sqlite:///{database_path}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


