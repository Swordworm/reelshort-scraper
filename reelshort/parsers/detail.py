import json
import logging
from reelshort.items import SeriesDetailItem

logger = logging.getLogger(__name__)


class DetailParser:
    PLACEHOLDER_TAGS = {"Playing Dumb"}

    def __init__(self, response):
        self.response = response
        self._data = self._load_next_data()

    def _load_next_data(self):
        raw = self.response.css("script#__NEXT_DATA__::text").get()
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError as e:
                logger.error("JSON decode failed on %s: %s", self.response.url, e)
        return None

    def get_item(self) -> SeriesDetailItem:
        if self._data:
            return self._item_from_json()
        logger.warning("No __NEXT_DATA__ on %s, returning empty item", self.response.url)
        return SeriesDetailItem()

    def _item_from_json(self) -> SeriesDetailItem:
        data = self._data
        if data is None:
            return SeriesDetailItem()
        try:
            m = data["props"]["pageProps"]["data"]
        except (KeyError, TypeError):
            logger.warning("Unexpected __NEXT_DATA__ structure on %s", self.response.url)
            m = {}

        seen = set()
        tags_parts = []
        for t in (m.get("tag_list") or []):
            text = t.get("text") if isinstance(t, dict) else None
            if text and text not in seen:
                seen.add(text)
                tags_parts.append(text)
        for text in (m.get("tag") or []):
            if isinstance(text, str) and text not in self.PLACEHOLDER_TAGS and text not in seen:
                seen.add(text)
                tags_parts.append(text)
        tags = ",".join(tags_parts) if tags_parts else None

        return SeriesDetailItem(
            series_url=self.response.url,
            series_title=m.get("book_title"),
            cover_image_url=m.get("book_pic"),
            description=m.get("special_desc"),
            episode_count=m.get("total"),
            tags=tags,
            book_genre=m.get("book_genre"),
            book_type=m.get("book_type"),
            book_source=m.get("book_source"),
            update_status=m.get("update_status"),
            read_count=m.get("read_count"),
            collect_count=m.get("collect_count"),
            online_at=m.get("online_at"),
            publish_at=m.get("publish_at"),
            has_dub=m.get("has_dub"),
        )
