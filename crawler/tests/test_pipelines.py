from unittest import mock

from crawler.pipelines import MongoPipeline

def test_attrs():
    pipeline = MongoPipeline()
    assert "imdb" == pipeline.collection_name


@mock.patch("crawler.pipelines.MongoPipeline._mongodb_db", return_value="test_crawler", new_callable=mock.PropertyMock)
def test_open_spider(_):
    pipeline = MongoPipeline()
    p_spider = mock.Mock()
    pipeline.open_spider(p_spider)

    assert "test_crawler" == pipeline.db.name
    p_spider.logger.info.assert_called_once_with("action=MongoPipeline, message=conecting to mongodb")


@mock.patch("crawler.pipelines.MongoPipeline.client")
def test_close_spider(p_client):
    pipeline = MongoPipeline()
    p_spider = mock.Mock()
    pipeline.close_spider(p_spider)

    assert p_client.close.called
    p_spider.logger.info.assert_called_once_with("action=MongoPipeline, message=closing the mongodb connection")


@mock.patch("crawler.pipelines.MongoPipeline._mongodb_db", return_value="test_crawler", new_callable=mock.PropertyMock)
def test_process_item(_):
    pipeline = MongoPipeline()
    p_spider = mock.Mock()
    pipeline.open_spider(p_spider)
    item = {
        "name": "The Shawshank Redemption",
        "position": "1",
        "year": "1994",
        "duration": "2h 22m",
        "rating": "9.3",
        "link": "https://imdb.com/title/tt0111161/?ref_=chttp_t_1",  # noqa
        "image": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg",  # noqa
    }
    pipeline.process_item(item, p_spider)
    mongo_item_id = item.pop("_id")
    p_spider.logger.info.assert_has_calls(
        [
            mock.call("action=MongoPipeline, message=conecting to mongodb"),
            mock.call(f"action=MongoPipeline, message=store item {item}"),
            mock.call(f"action=MongoPipeline, message=stored {mongo_item_id} item"),
        ]
    )
    assert 3 == p_spider.logger.info.call_count


@mock.patch("crawler.pipelines.MongoPipeline._mongodb_db", return_value="test_crawler", new_callable=mock.PropertyMock)
def test_process_item_dont_duplicated_item(_):
    pipeline = MongoPipeline()
    p_spider = mock.Mock()
    pipeline.open_spider(p_spider)
    item = {
        "name": "The Shawshank Redemption",
        "position": "1",
        "year": "1994",
        "duration": "2h 22m",
        "rating": "9.3",
        "link": "https://imdb.com/title/tt0111161/?ref_=chttp_t_1",  # noqa
        "image": "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg",  # noqa
    }
    pipeline.process_item(item, p_spider)
    mongo_item_id = item.pop("_id")
    pipeline.process_item(item, p_spider)

    p_spider.logger.info.assert_has_calls(
        [
            mock.call("action=MongoPipeline, message=conecting to mongodb"),
            mock.call(f"action=MongoPipeline, message=store item {item}"),
            mock.call(f"action=MongoPipeline, message=stored {mongo_item_id} item"),
            mock.call(f"action=MongoPipeline, message=store item {item}"),
            mock.call(f"action=MongoPipeline, message=the item already exists"),
        ]
    )
    assert 5 == p_spider.logger.info.call_count