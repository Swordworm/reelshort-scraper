from sqlalchemy import select
from reelshort.database import init_db, get_session
from reelshort.models import Series


class SQLitePipeline:
    def open_spider(self, spider):
        init_db()
        self.session = get_session()

    def close_spider(self, spider):
        self.session.close()

    def process_item(self, item, spider):
        row = self.session.execute(
            select(Series).where(Series.series_url == item["series_url"])
        ).scalar_one_or_none()
        if row is None:
            row = Series(series_url=item["series_url"])
            self.session.add(row)
        for field, value in item.items():
            setattr(row, field, value)
        row.detail_scraped = True
        self.session.commit()
        return item
