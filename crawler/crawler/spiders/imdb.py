import requests
import scrapy

from pathlib import Path


class ImdbSpider(scrapy.Spider):
    name = "imdb"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"]

    _BASE_URL = "https://imdb.com"
    _CSS_SUMMARY_ITEM = "div.ipc-metadata-list-summary-item__c"
    _SCREENSHOT_DIR = Path(__file__).parent.parent.parent
    _SPLASH_URL = "http://splash:8050/run"
    _LUA_SCRIPT = """
    splash:go(args.url)
    splash.set_viewport_full()
    return splash:png()
    """

    def parse(self, response):
        self.logger.info("action=parse, message=starting parse")
        try:
            for movie in response.css("li.ipc-metadata-list-summary-item"):
                yield self.extraction(movie)
        finally:
            self.take_screenshot()

    def _get_name_and_position(self, raw_name):
        self.logger.info(f"action=_get_name_and_position, message={raw_name}")
        splitted_raw_name = raw_name.split(" ")
        if "." in splitted_raw_name[0]:
            position = splitted_raw_name[0].replace(".", "")
            name = " ".join(splitted_raw_name[1:])
        else:
            position = None
            name = " ".join(splitted_raw_name)
        return name, position

    def extraction(self, movie):
        self.logger.info("action=extraction, message=starting the data extraction")
        data = {}
        raw_name = movie.css(f"{self._CSS_SUMMARY_ITEM} h3.ipc-title__text::text").extract_first()

        name, position = self._get_name_and_position(raw_name)
        raw_metadata = movie.css(f"{self._CSS_SUMMARY_ITEM} span.cli-title-metadata-item::text").getall()

        data["name"] = name
        data["position"] = position
        data["year"] = raw_metadata[0]
        data["duration"] = raw_metadata[1]
        data["rating"] = movie.css(f"{self._CSS_SUMMARY_ITEM} span.ipc-rating-star::attr(aria-label)").get()
        data["rating"] = data["rating"].replace("IMDb rating: ", "")

        movie_link = movie.css(f"{self._CSS_SUMMARY_ITEM} a.ipc-title-link-wrapper::attr(href)").get()
        if "imdb.com" in movie_link:
            data["link"] = movie_link
        else:
            data["link"] = "{}{}".format(self._BASE_URL, movie_link)

        data["image"] = movie.css("div.cli-poster-container img::attr(src)").extract_first()
        return data

    def take_screenshot(self):
        self.logger.info("action=take_screenshot, message=starting to take a screenshot")
        resp = requests.post(self._SPLASH_URL, json={
            "lua_source": self._LUA_SCRIPT,
            "url": self.start_urls[0]
        })
        png_data = resp.content
        filename = f"{self._SCREENSHOT_DIR}/imdb_com.png"
        Path(filename).write_bytes(png_data)
        self.logger.info("action=take_screenshot, message=done")