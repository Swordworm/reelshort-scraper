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
        tags = ",".join(t["text"] for t in tag_list if t.get("text"))

        return SeriesItem(
            episode_count=str(m.get("total", "")),
            tags=tags,
            book_genre=str(m.get("book_genre", "")),
            book_type=str(m.get("book_type", "")),
            book_source=str(m.get("book_source", "")),
            update_status=str(m.get("update_status", "")),
            read_count=str(m.get("read_count", "")),
            collect_count=str(m.get("collect_count", "")),
            online_at=str(m.get("online_at", "")),
            publish_at=str(m.get("publish_at", "")),
            has_dub=bool(m.get("has_dub", False)),
        )