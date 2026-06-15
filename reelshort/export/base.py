from abc import ABC, abstractmethod
from scrapy.commands import ScrapyCommand
from sqlalchemy import select
from reelshort.database import init_db, get_session
from reelshort.models import Series


class BaseExportCommand(ScrapyCommand, ABC):
    requires_project = True

    @abstractmethod
    def export(self, rows: list, settings) -> None:
        ...

    def run(self, args, opts):
        init_db()
        with get_session() as session:
            rows = session.execute(select(Series)).scalars().all()
        self.export(rows, self.settings)
