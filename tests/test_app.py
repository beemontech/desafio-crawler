import pymongo
from decouple import config


def test_empty_home(client):
    response = client.get("/")
    assert "Sorry, we're empty" in str(response.data)


def test_home(client):
    mongoclient = pymongo.MongoClient(config("MONGODB_URI"))
    db = mongoclient["test_crawler"]

    item = {
        "name": "The Shawshank Redemption",
        "position": "1",
        "year": "1994",
        "duration": "2h 22m",
        "rating": "9.3",
        "link": "https://imdb.com/title/tt0111161/?ref_=chttp_t_1",  # noqa
        "image": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg",  # noqa
    }
    db[config("MONGODB_COLLECTION")].insert_one(item)

    response = client.get("/")
    content = str(response.data)
    assert "Sorry, we're empty" not in content
    assert item["name"] in content
    assert item["position"] in content
    assert item["year"] in content
    assert item["duration"] in content
    assert item["rating"] in content
    assert item["link"] in content
    assert item["image"] in content
