from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, Boolean, Integer, DateTime, ForeignKey, Index
from reelshort.models.base import Base


class Series(Base):
    __tablename__ = "series"

    id: Mapped[int] = mapped_column(primary_key=True)
    listing_id: Mapped[int] = mapped_column(Integer, ForeignKey("listing.id"))
    book_id: Mapped[str] = mapped_column(String, unique=True, index=True)
    series_url: Mapped[str] = mapped_column(String)
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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    scraped_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    exception: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
