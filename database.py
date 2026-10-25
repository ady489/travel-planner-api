from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

# Use a local SQLite file
SQLALCHEMY_DATABASE_URL = "sqlite:///./travel.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Database model for a trip
class Trip(Base):
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, index=True)
    days = Column(Integer)

# Create tables on startup
Base.metadata.create_all(bind=engine)