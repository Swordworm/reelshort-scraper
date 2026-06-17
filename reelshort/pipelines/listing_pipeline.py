from datetime import datetime, timezone
from sqlalchemy import select
from reelshort.database import init_db, get_session
from reelshort.items import ListingItem
from reelshort.models import Listing, Series


class ListingPipeline:
    def open_spider(self):
        init_db()
        self._session = get_session()

    def close_spider(self):
        self._session.close()

    def process_item(self, item):
        if not isinstance(item, ListingItem):
            return item

        now = datetime.now(timezone.utc)

        row = self._session.execute(
            select(Listing).where(Listing.page_url == item["page_url"])
        ).scalar_one_or_none()

        if row is None:
            row = Listing(
                page_url=item["page_url"],
                page_number=item["page_number"],
                created_at=now,
            )
            self._session.add(row)

        row.scraped_at = item.get("scraped_at") or now
        row.exception = item.get("exception")

        self._session.flush()
        listing_id = row.id

        for url in item.get("series") or []:
            book_id = url.rstrip("/").split("-")[-1]
            row = self._session.execute(
                select(Series).where(Series.book_id == book_id)
            ).scalar_one_or_none()
            if row is None:
                self._session.add(Series(
                    book_id=book_id,
                    series_url=url,
                    listing_id=listing_id,
                    created_at=now,
                ))
            elif row.series_url != url:
                row.series_url = url

        self._session.commit()
        return item
