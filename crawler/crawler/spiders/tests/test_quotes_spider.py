import os
import pytest
import base64
from scrapy.http import HtmlResponse
from crawler.spiders.quotes import QuotesSpider
from scrapy_splash import SplashRequest
from .html_itens import HTML_QUOTE, NEXT_PAGE_HTML


class TestQuotesSpider:
    @pytest.fixture(autouse=True)
    def setup_method_fixture(self):
        self.spider = QuotesSpider()
        self.url = "https://quotes.toscrape.com"

    def test_start_requests(self):
        requests = list(self.spider.start_requests())
        assert len(requests) == len(self.spider.start_urls)
        for request in requests:
            assert isinstance(request, SplashRequest)

    def test_create_splash_request(self, mocker):
        mock_splash_request = mocker.patch("crawler.spiders.quotes.SplashRequest")
        self.spider.create_splash_request(self.url, self.spider.parse)

        mock_splash_request.assert_called_once_with(
            self.url,
            self.spider.parse,
            endpoint="render.json",
            args={
                "wait": self.spider.SPLASH_WAIT_TIME,
                "html": 1,
                "png": 1,
                "render_all": 1,
            },
        )

    def test_parse_with_next_page(self):
        request = self.spider.create_splash_request(self.url, self.spider.parse)

        response = HtmlResponse(
            url=self.url, request=request, body=NEXT_PAGE_HTML, encoding="utf-8"
        )

        results = list(self.spider.parse(response))
        assert len(results) == 1
        assert isinstance(results[0], SplashRequest)
        assert results[0].url == self.url + "/page/2/"

    def test_extract_quotes_without_quotes(self):
        request = self.spider.create_splash_request(self.url, self.spider.parse)
        response = HtmlResponse(
            url=self.url, request=request, body="<html></html>", encoding="utf-8"
        )

        results = list(self.spider.extract_quotes(response))
        assert len(results) == 0

    def test_parse(self):
        request = self.spider.create_splash_request(self.url, self.spider.parse)
        response = HtmlResponse(
            url=self.url, request=request, body="<html></html>", encoding="utf-8"
        )

        results = list(self.spider.parse(response))
        assert len(results) == 0

    def test_extract_quotes(self):
        request = self.spider.create_splash_request(self.url, self.spider.parse)

        response = HtmlResponse(
            url=self.url, request=request, body=HTML_QUOTE, encoding="utf-8"
        )

        results = list(self.spider.extract_quotes(response))
        assert len(results) == 1
        assert results[0]["text"] == '"Hello, World!"'
        assert results[0]["author"] == "John Doe"
        assert results[0]["tags"] == ["tag1", "tag2"]

    # def test_save_screenshot(self, mocker):
    #     mock_open = mocker.mock_open()
    #     mocker.patch("crawler.spiders.quotes.open", new_callable=mock_open)
    #     request = self.spider.create_splash_request(self.url, self.spider.parse)
    #     response = HtmlResponse(
    #         url=self.url, request=request, body=HTML_QUOTE, encoding="utf-8"
    #     )
    #     response.data = {"png": base64.b64encode(b"test").decode("utf-8")}

    #     self.spider.save_screenshot(response)

    #     filename = f'{self.spider.SCREENSHOT_PATH}/screenshot_{self.url.replace("https://", "").replace("/", "_")}.png'
    #     mock_open.assert_called_once_with(filename, "wb")
    #     handle = mock_open()
    #     handle.write.assert_called_once_with(b"test")
