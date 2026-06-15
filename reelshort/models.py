from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Integer


class Base(DeclarativeBase):
    pass


class Series(Base):
    __tablename__ = "series"

    id              : Mapped[int]           = mapped_column(primary_key=True)
    series_url      : Mapped[str]           = mapped_column(String, unique=True)
    series_title    : Mapped[Optional[str]] = mapped_column(String)
    cover_image_url : Mapped[Optional[str]] = mapped_column(String)
    description     : Mapped[Optional[str]] = mapped_column(Text)
    episode_count   : Mapped[Optional[str]] = mapped_column(String)
    tags            : Mapped[Optional[str]] = mapped_column(Text)
    book_genre      : Mapped[Optional[str]] = mapped_column(String)
    book_type       : Mapped[Optional[str]] = mapped_column(String)
    book_source     : Mapped[Optional[str]] = mapped_column(String)
    update_status   : Mapped[Optional[str]] = mapped_column(String)
    read_count      : Mapped[Optional[str]] = mapped_column(String)
    collect_count   : Mapped[Optional[str]] = mapped_column(String)
    online_at       : Mapped[Optional[str]] = mapped_column(String)
    publish_at      : Mapped[Optional[str]] = mapped_column(String)
    has_dub         : Mapped[Optional[bool]] = mapped_column(Boolean)
    detail_scraped  : Mapped[bool]           = mapped_column(Boolean, default=False)
