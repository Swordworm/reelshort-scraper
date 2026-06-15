import json
from reelshort.items import SeriesItem

_UPDATE_STATUS = {1: "Ongoing", 2: "Completed"}


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
        return self._item_from_html()

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

        status_code = m.get("update_status")
        status = _UPDATE_STATUS.get(status_code, str(status_code) if status_code is not None else "")

        return SeriesItem(
            episode_count=str(m.get("total", "")),
            status=status,
            genre=str(m.get("book_genre", "")),
            tags=tags,
        )

    def _item_from_html(self) -> SeriesItem:
        episode_count = self.response.css("[class*='episode']::text, [class*='count']::text").get(default="").strip()
        status = self.response.css("[class*='status']::text").get(default="").strip()
        genre = self.response.css("[class*='genre']::text, [class*='category']::text").get(default="").strip()
        tags = ",".join(t.strip() for t in self.response.css("[class*='tag']::text").getall() if t.strip())
        return SeriesItem(episode_count=episode_count, status=status, genre=genre, tags=tags)
