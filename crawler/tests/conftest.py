import os
import pytest

from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse


@pytest.fixture
def fake_imdb_response():
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    request = Request(url=url)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, "resources", "imdb.html")

    with open(file_path, "r") as f:
        response = HtmlResponse(
            url=url,
            request=request,
            body=f.read().encode(),
            encoding='utf-8'
        )
    return response