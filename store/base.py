import sqlalchemy
from sqlalchemy import create_engine

from store.models import DATABASE_URL

engine = create_engine(DATABASE_URL)


def connect() -> sqlalchemy.engine.Connection:
    return engine.connect()
