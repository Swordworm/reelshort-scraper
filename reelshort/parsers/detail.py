import json
from reelshort.items import SeriesItem


class DetailParser:
    def __init__(self, response):
        self.response = response
        self._data = self._load_next_data()

    def _load_next_data(self):
        raw = self.response.css("script#__NEXT_DATA__::text").get()
        if raw:
            try:
                return json.loads(raw)
            except json.JSONDecodeError:
                pass
        return None

    def get_item(self) -> SeriesItem:
        if self._data:
            return self._item_from_json()
        return SeriesItem()

    def _item_from_json(self) -> SeriesItem:
        data = self._data
        if data is None:
            return SeriesItem()
        try:
            m = data["props"]["pageProps"]["data"]
        except (KeyError, TypeError):
            m = {}

        tag_list = m.get("tag_list") or []
        tags_parts = [t["text"] for t in tag_list if t.get("text")]
        tags = ",".join(tags_parts) if tags_parts else None

        return SeriesItem(
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
