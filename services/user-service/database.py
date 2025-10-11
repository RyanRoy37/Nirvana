from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = "postgresql://postgres:admin@127.0.0.1:5433/nirvana1"

engine = create_engine(POSTGRES_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

from pymongo import MongoClient

# Connect to MongoDB (adjust host/port as needed)
client = MongoClient("mongodb://127.0.0.1:27017/")

# Database and collection
mongo_db = client["dev_hive"]
projects_collection = mongo_db["projects_implementation"]
