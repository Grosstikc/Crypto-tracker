import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Float, Boolean
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define user model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, autoincrement=True)
    chat_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True, nullable=True)  # add username clearly

# Define alerts model
class Alert(Base):
    __tablename__ = 'alerts'
    id = Column(Integer, primary_key=True, index=True)
    user_chat_id = Column(String, primary_key=True, index=True)
    crypto = Column(String, index=True)
    currency = Column(String, index=True)
    price = Column(Float)
    direction = Column(String)
    triggered = Column(Boolean, default=False)

# Create tables
Base.metadata.create_all(bind=engine)
