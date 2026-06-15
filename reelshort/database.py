from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from reelshort.models import Base

ENGINE = create_engine("sqlite:///reelshort.db")


def init_db() -> None:
    Base.metadata.create_all(ENGINE)


def get_session() -> Session:
    return Session(ENGINE)
