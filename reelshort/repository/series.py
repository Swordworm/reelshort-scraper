from sqlalchemy import select
from reelshort.database import get_session
from reelshort.models import Series


def get_scraped_urls() -> set[str]:
    with get_session() as session:
        return set(
            session.execute(
                select(Series.series_url).where(Series.detail_scraped.is_(True))
            ).scalars().all()
        )
