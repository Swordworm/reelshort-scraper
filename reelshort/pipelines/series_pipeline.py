import logging
from datetime import datetime, timezone
from sqlalchemy import select
from reelshort.database import get_session
from reelshort.items import SeriesDetailItem
from reelshort.models import Series

logger = logging.getLogger(__name__)


class SeriesPipeline:
    def open_spider(self):
        self._session = get_session()

    def close_spider(self):
        self._session.close()

    def process_item(self, item):
        if not isinstance(item, SeriesDetailItem):
            return item

        row = self._session.execute(
            select(Series).where(Series.id == item["series_id"])
        ).scalar_one_or_none()

        if row is None:
            logger.error("Series id=%s not found in DB", item["series_id"])
            return item

        try:
            if item.get("exception"):
                row.exception = item["exception"]
            else:
                row.series_title = item.get("series_title")
                row.cover_image_url = item.get("cover_image_url")
                row.description = item.get("description")
                row.episode_count = item.get("episode_count")
                row.tags = item.get("tags")
                row.book_genre = item.get("book_genre")
                row.book_type = item.get("book_type")
                row.book_source = item.get("book_source")
                row.update_status = item.get("update_status")
                row.read_count = item.get("read_count")
                row.collect_count = item.get("collect_count")
                row.online_at = item.get("online_at")
                row.publish_at = item.get("publish_at")
                row.has_dub = item.get("has_dub")
                row.scraped_at = datetime.now(timezone.utc)
                row.exception = None

            self._session.commit()
        except Exception:
            self._session.rollback()
            logger.exception("Failed to save series id=%s", item.get("series_id"))

        return item
