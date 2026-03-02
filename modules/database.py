import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# This loads the values from your .env file
load_dotenv()

# Grab the database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the connection to the database
engine = create_engine(DATABASE_URL)

# A session is like opening a connection to run queries
SessionLocal = sessionmaker(bind=engine)

# Base is the starting point for defining tables
Base = declarative_base()


# This class = one table in the database called "matches"
class Match(Base):
    __tablename__ = "matches"

    id = Column(Integer, primary_key=True, index=True)  # auto ID
    home_team = Column(String)
    away_team = Column(String)
    home_score = Column(Integer)
    away_score = Column(Integer)
    date = Column(String)


# This class = one table in the database called "players"
class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    team = Column(String)
    position = Column(String)   # GK, DF, MF, FW
    goals = Column(Integer)
    assists = Column(Integer)
    cost = Column(Float)            # fantasy cost in £M
    expected_points = Column(Float) # fantasy expected points


def create_tables():
    # This actually creates the tables in PostgreSQL
    Base.metadata.create_all(bind=engine)


def get_db():
    # This is used by FastAPI to open/close db connections automatically
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()