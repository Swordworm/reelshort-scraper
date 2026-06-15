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
        return self._item_from_html()

    def _item_from_json(self) -> SeriesItem:
        # TODO: adjust path once real JSON structure is known
        try:
            page_props = self._data["props"]["pageProps"]
            m = (
                page_props.get("movieDetail")
                or page_props.get("movie")
                or page_props.get("data")
                or {}
            )
        except (KeyError, TypeError):
            m = {}

        tags_raw = m.get("tags") or m.get("label") or []
        if isinstance(tags_raw, list):
            tags = ",".join(str(t) for t in tags_raw)
        else:
            tags = str(tags_raw)

        return SeriesItem(
            episode_count=str(m.get("episodeCount") or m.get("episode_count") or m.get("episodes") or ""),
            status=m.get("status") or m.get("updateStatus") or "",
            genre=m.get("genre") or m.get("category") or "",
            tags=tags,
        )

    def _item_from_html(self) -> SeriesItem:
        # TODO: tune selectors after inspecting rendered HTML
        episode_count = self.response.css("[class*='episode']::text, [class*='count']::text").get(default="").strip()
        status = self.response.css("[class*='status']::text").get(default="").strip()
        genre = self.response.css("[class*='genre']::text, [class*='category']::text").get(default="").strip()
        tags_list = self.response.css("[class*='tag']::text").getall()
        tags = ",".join(t.strip() for t in tags_list if t.strip())

        return SeriesItem(
            episode_count=episode_count,
            status=status,
            genre=genre,
            tags=tags,
        )
