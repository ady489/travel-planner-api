from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# This creates a file called 'travel.db' in your folder
SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# This defines what a "Trip" looks like in the database
class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    days = Column(Integer)

# Create the database tables
Base.metadata.create_all(bind=engine)