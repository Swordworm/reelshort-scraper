from datetime import datetime, timezone
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, DateTime, Integer
from reelshort.models.base import Base


class Listing(Base):
    __tablename__ = "listing"

    id: Mapped[int] = mapped_column(primary_key=True)
    page_url: Mapped[str] = mapped_column(String, unique=True)
    page_number: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    scraped_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    exception: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
