from typing import Optional
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Integer


class Base(DeclarativeBase):
    pass


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    series_url: Mapped[str] = mapped_column(String, unique=True)
    series_title: Mapped[Optional[str]] = mapped_column(String)
    cover_image_url: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    episode_count: Mapped[Optional[int]] = mapped_column(Integer)
    tags: Mapped[Optional[str]] = mapped_column(Text)
    book_genre: Mapped[Optional[int]] = mapped_column(Integer)
    book_type: Mapped[Optional[int]] = mapped_column(Integer)
    book_source: Mapped[Optional[int]] = mapped_column(Integer)
    update_status: Mapped[Optional[int]] = mapped_column(Integer)
    read_count: Mapped[Optional[int]] = mapped_column(Integer)
    collect_count: Mapped[Optional[int]] = mapped_column(Integer)
    online_at: Mapped[Optional[int]] = mapped_column(Integer)
    publish_at: Mapped[Optional[int]] = mapped_column(Integer)
    has_dub: Mapped[Optional[bool]] = mapped_column(Boolean)
    detail_scraped: Mapped[bool] = mapped_column(Boolean, default=False)
