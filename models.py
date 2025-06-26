from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# This will create a file 'usage.db' in your folder
DATABASE_URL = "sqlite:///usage.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Usage(Base):
    __tablename__ = "usage"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True)
    mac_address = Column(String)
    start_time = Column(DateTime)
    usage_time = Column(String)
    upload = Column(Float)
    download = Column(Float)