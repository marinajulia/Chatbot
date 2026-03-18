import os 
from dotenv import load_dotenv
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

load_dotenv()
database_url = os.getenv("DATABASE_URL")

engine = create_engine(database_url, echo=False)

Base = declarative_base() 