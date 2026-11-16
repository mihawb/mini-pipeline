from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
    os.environ["POSTGRES_USER"],
    os.environ["POSTGRES_PASSWORD"],
    os.environ["POSTGRES_HOST"],
    os.environ["POSTGRES_PORT"],
    os.environ["POSTGRES_DB"],
)
engine: Engine = create_engine(DATABASE_URL, pool_pre_ping=True)
