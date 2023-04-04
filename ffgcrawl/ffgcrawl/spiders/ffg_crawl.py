import scrapy
from scrapy.http.response.html import HtmlResponse
from scrapy.http.response import Response
from scrapy.spiders import logging

from ..items import PdfItem, TextItem

LOGGER = logging.getLogger(__name__)


class FfgCrawlSpider(scrapy.Spider):
    name = "ffg-crawl"
    allowed_domains = ["fukuoka-fg.com"]
    start_urls = ["https://www.fukuoka-fg.com/"]

    def __init__(self, max_depth=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.max_depth = int(max_depth)

    def parse(self, response: HtmlResponse | Response):
        if isinstance(response, HtmlResponse):
            if response.meta["depth"] < self.max_depth:
                atags = response.xpath("//a")
                links = [a.attrib["href"] for a in atags if "href" in a.attrib]
                for l in links:
                    if l[:1] == "/":
                        yield response.follow(l, self.parse)
            
            texts = [t.get() for t in response.xpath("//body//text()[not(parent::script)]")]
            title = response.xpath("//title/text()").get() or ""
            
            yield TextItem(response.url, title, "".join(texts))
            return
            

        if isinstance(response, Response):
            ty = response.headers[b"Content-Type"]
            if ty is None:
                LOGGER.warning("Content-Type is not set")
                return
            ty2 = ty.decode()
            if ty2 == "application/pdf":
                yield PdfItem(response.url, response.body)
            else:
                LOGGER.warning("Unknown content type: %s", ty2)
            return

        LOGGER.warning(f"Unknown response type: %s", type(response))
