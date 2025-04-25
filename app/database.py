import os

import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv("DB_USER", "postgres")
db_pass = os.getenv("DB_PASS", "postgres")
db_name = os.getenv("DB_NAME", "lumovus")
db_host = os.getenv("DB_HOST", "localhost")
db_port = int(os.getenv("DB_PORT", 5432))

SQLALCHEMY_DATABASE_URL = sqlalchemy.engine.url.URL.create(
    drivername="postgresql",
    username=db_user,
    password=db_pass,
    host=db_host,
    port=db_port,
    database=db_name
)
engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
