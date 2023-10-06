from unittest import mock

from crawler.spiders.imdb import ImdbSpider


def test_imdb_attrs():
    spider = ImdbSpider()

    assert "imdb" == spider.name
    assert ["imdb.com"] == spider.allowed_domains
    assert ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"] == spider.start_urls

    assert "https://imdb.com" == spider._BASE_URL
    assert "div.ipc-metadata-list-summary-item__c" == spider._CSS_SUMMARY_ITEM


def test_imdb_get_name_and_position():
    spider = ImdbSpider()

    assert ("The Godfather", "2") == spider._get_name_and_position("2. The Godfather")
    assert ("The Godfather", None) == spider._get_name_and_position("The Godfather")
    assert ("The", None) == spider._get_name_and_position("The")


def test_parse(fake_imdb_response):
    spider = ImdbSpider()
    result = next(spider.parse(fake_imdb_response))

    assert result["name"] == "The Shawshank Redemption"
    assert result["position"] == "1"
    assert result["year"] == "1994"
    assert result["duration"] == "2h 22m"
    assert result["rating"] == "9.3"
    assert result["link"] == "https://imdb.com/title/tt0111161/?ref_=chttp_t_1"  # noqa
    assert result["image"] == "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg"  # noqa


def test_logger(fake_imdb_response):
    spider = ImdbSpider()
    with mock.patch("crawler.spiders.imdb.ImdbSpider.logger") as p_logger:
        next(spider.parse(fake_imdb_response))
        p_logger.info.assert_has_calls([
            mock.call("action=parse, message=starting parse"),
            mock.call("action=extraction, message=starting the data extraction"),
            mock.call("action=_get_name_and_position, message=1. The Shawshank Redemption"),
        ])