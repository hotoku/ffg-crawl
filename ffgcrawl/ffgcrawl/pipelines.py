from typing import Any
from datetime import datetime

from scrapy.spiders import logging

from .db import Db
from .items import PdfItem, TextItem

LOGGER = logging.getLogger(__name__)


def save_pdf(item: PdfItem):
    con = Db.connect()
    con.execute("""
insert into pdfs (url, content, created_at) values (?, ?, ?)
""", (item.url, item.content, datetime.now().isoformat()))
    con.commit()

def save_text(item: TextItem):
    con = Db.connect()
    con.execute("""
insert into texts (url, content, created_at) values (?, ?, ?)
""", (item.url, item.content, datetime.now().isoformat()))
    con.commit()


class FfgcrawlPipeline:
    def process_item(self, item: PdfItem | TextItem | Any, _):
        if isinstance(item, PdfItem):
            save_pdf(item)
        elif isinstance(item, TextItem):
            save_text(item)
        else:
            LOGGER.warning("unknown item type: %s", type(item))
        return item

