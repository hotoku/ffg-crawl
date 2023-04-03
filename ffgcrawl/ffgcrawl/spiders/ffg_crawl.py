import scrapy


class FfgCrawlSpider(scrapy.Spider):
    name = "ffg-crawl"
    allowed_domains = ["fukuoka-fg.com"]
    start_urls = ["http://fukuoka-fg.com/"]

    def parse(self, response):
        pass
