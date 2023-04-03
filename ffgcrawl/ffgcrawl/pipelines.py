from typing import Any

from scrapy.spiders import logging
from .items import PdfItem, TextItem

LOGGER = logging.getLogger(__name__)


class FfgcrawlPipeline:
    def process_item(self, item: PdfItem | TextItem | Any, _):
        if isinstance(item, PdfItem):
            print("pdf", item.url)
        elif isinstance(item, TextItem):
            print("text", item.url)
        else:
            LOGGER.warning("unknown item type: %s", type(item))
        return item
