import os
import scrapy
import base64
from scrapy_splash import SplashRequest
from crawler.items import QuoteItem


class QuotesSpider(scrapy.Spider):
    name = "quotes"
    allowed_domains = ["quotes.toscrape.com"]
    start_urls = ["https://quotes.toscrape.com/"]
    SCREENSHOT_PATH = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "screenshots"
    )
    SPLASH_WAIT_TIME = 0.5

    def start_requests(self):
        for url in self.start_urls:
            yield self.create_splash_request(url, self.parse)

    def create_splash_request(self, url, callback):
        return SplashRequest(
            url,
            callback,
            endpoint="render.json",
            args={"wait": self.SPLASH_WAIT_TIME, "html": 1, "png": 1, "render_all": 1},
        )

    def parse(self, response):
        self.logger.info("Parse function called on %s", response.url)
        self.save_screenshot(response)
        yield from self.extract_quotes(response)
        next_page = response.css("li.next a::attr(href)").get()
        if next_page is not None:
            yield self.create_splash_request(response.urljoin(next_page), self.parse)

    def save_screenshot(self, response):
        screenshot = response.data["png"]
        imgdata = base64.b64decode(screenshot)
        filename = f'{self.SCREENSHOT_PATH}/screenshot_{response.url.replace("https://", "").replace("/", "_")}.png'
        with open(filename, "wb") as f:
            f.write(imgdata)
        self.logger.info(f"Screenshot salvo como {filename}")

    def extract_quotes(self, response):
        for quote in response.css("div.quote"):
            self.logger.info(
                "Processing quote from : %s", quote.css("span small::text").get()
            )
            item = QuoteItem()
            item["text"] = quote.css("span.text::text").get()
            item["author"] = quote.css("span small::text").get()
            item["tags"] = quote.css("div.tags a.tag::text").getall()
            yield item
