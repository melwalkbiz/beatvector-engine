from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Database URL: postgresql://user:password@host/dbname
DB_URL = os.getenv("DATABASE_URL", "postgresql+psycopg2://beatuser:Handsome1@localhost/beatvector")

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Metadata(Base):
    __tablename__ = 'metadata'
    id = Column(Integer, primary_key=True, index=True)
    query = Column(String, index=True)
    discogs = Column(JSON)
    youtube = Column(JSON)

# Create tables
Base.metadata.create_all(bind=engine)
