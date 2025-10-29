from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker

# Update only your password below after unzipping
DATABASE_URL = "postgresql://postgres:Aleeza786@localhost:5432/bike_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
metadata = MetaData()
