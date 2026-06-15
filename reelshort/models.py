from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Boolean


class Base(DeclarativeBase):
    pass


class Series(Base):
    __tablename__ = "series"

    id              : Mapped[int]           = mapped_column(primary_key=True)
    series_url      : Mapped[str]           = mapped_column(String, unique=True)
    series_title    : Mapped[Optional[str]] = mapped_column(String)
    cover_image_url : Mapped[Optional[str]] = mapped_column(String)
    description     : Mapped[Optional[str]] = mapped_column(Text)
    genre           : Mapped[Optional[str]] = mapped_column(String)
    episode_count   : Mapped[Optional[str]] = mapped_column(String)
    status          : Mapped[Optional[str]] = mapped_column(String)
    tags            : Mapped[Optional[str]] = mapped_column(String)
    detail_scraped  : Mapped[bool]          = mapped_column(Boolean, default=False)
