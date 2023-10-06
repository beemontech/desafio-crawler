from unittest import mock

from crawler.spiders.imdb import ImdbSpider


def test_imdb_attrs():
    spider = ImdbSpider()

    assert "imdb" == spider.name
    assert ["imdb.com"] == spider.allowed_domains
    assert ["https://www.imdb.com/chart/top/?ref_=nv_mv_250"] == spider.start_urls

    assert "https://imdb.com" == spider._BASE_URL
    assert "div.ipc-metadata-list-summary-item__c" == spider._CSS_SUMMARY_ITEM

    assert "/app/crawler" == str(spider._SCREENSHOT_DIR)
    assert "http://splash:8050/run" == spider._SPLASH_URL
    assert """
    splash:go(args.url)
    splash.set_viewport_full()
    return splash:png()
    """ == spider._LUA_SCRIPT


def test_imdb_get_name_and_position():
    spider = ImdbSpider()

    assert ("The Godfather", "2") == spider._get_name_and_position("2. The Godfather")
    assert ("The Godfather", None) == spider._get_name_and_position("The Godfather")
    assert ("The", None) == spider._get_name_and_position("The")


def test_parse(fake_imdb_response):
    spider = ImdbSpider()
    with mock.patch("crawler.spiders.imdb.ImdbSpider.take_screenshot") as p_take_screenshot:
        result = next(spider.parse(fake_imdb_response))

        assert result["name"] == "The Shawshank Redemption"
        assert result["position"] == "1"
        assert result["year"] == "1994"
        assert result["duration"] == "2h 22m"
        assert result["rating"] == "9.3"
        assert result["link"] == "https://imdb.com/title/tt0111161/?ref_=chttp_t_1"  # noqa
        assert result["image"] == "https://m.media-amazon.com/images/M/MV5BNDE3ODcxYzMtY2YzZC00NmNlLWJiNDMtZDViZWM2MzIxZDYwXkEyXkFqcGdeQXVyNjAwNDUxODI@._V1_QL75_UX140_CR0,1,140,207_.jpg"  # noqa

        assert p_take_screenshot.called


def test_logger(fake_imdb_response):
    with mock.patch("crawler.spiders.imdb.ImdbSpider.take_screenshot") as p_take_screenshot:
        spider = ImdbSpider()
        with mock.patch("crawler.spiders.imdb.ImdbSpider.logger") as p_logger:
            next(spider.parse(fake_imdb_response))

            p_logger.info.assert_has_calls([
                mock.call("action=parse, message=starting parse"),
                mock.call("action=extraction, message=starting the data extraction"),
                mock.call("action=_get_name_and_position, message=1. The Shawshank Redemption"),
                mock.call("action=parse, message=starting to take a screenshot"),
            ])
            assert 4 == p_logger.info.call_count

        assert p_take_screenshot.called


def test_call_take_screenshot(fake_imdb_response):
    spider = ImdbSpider()
    with mock.patch("crawler.spiders.imdb.ImdbSpider.take_screenshot") as p_take_screenshot:
        next(spider.parse(fake_imdb_response))

        assert p_take_screenshot.called


def test_take_screenshot():
    spider = ImdbSpider()
    with mock.patch("crawler.spiders.imdb.requests") as p_requests:
        with mock.patch("crawler.spiders.imdb.Path") as p_path:
            mock_response = mock.Mock()
            mock_response.content = b"foo"
            p_requests.post.return_value = mock_response
            spider.take_screenshot()

            p_requests.post.assert_called_once_with(
                spider._SPLASH_URL, json={"lua_source": spider._LUA_SCRIPT, "url": spider.start_urls[0]}
            )
            p_path.assert_called_once_with(f"{spider._SCREENSHOT_DIR}/imdb_com.png")
            p_path().write_bytes.assert_called_once_with(b"foo")