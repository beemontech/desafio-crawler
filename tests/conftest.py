import os
import pytest
import pymongo

from decouple import config
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse

from app import create_app


@pytest.fixture
def fake_imdb_response():
    url = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    request = Request(url=url)

    base_dir = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(base_dir, "resources", "imdb.html")

    with open(file_path, "r") as f:
        response = HtmlResponse(url=url, request=request, body=f.read().encode(), encoding="utf-8")
    return response


@pytest.fixture(autouse=True)
def clearup_mongodb():
    client = pymongo.MongoClient(config("MONGODB_URI"))
    db = client["test_crawler"]
    for collection_name in db.list_collection_names():
        collection = db[collection_name]

        if not collection.name.startswith("system."):
            collection.drop()
    client.close()


@pytest.fixture()
def app(clearup_mongodb):
    app = create_app()
    app.config.update(
        {
            "MONGODB_DB": "test_crawler",
        }
    )
    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
