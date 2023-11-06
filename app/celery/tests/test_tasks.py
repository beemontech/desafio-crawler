from app.celery.tasks import run_spider, CRAWLER_PATH


def test_run_spider(mocker):
    mock_check_output = mocker.patch("subprocess.check_output")
    run_spider()

    mock_check_output.assert_called_once_with(
        ["scrapy", "crawl", "quotes"], cwd=CRAWLER_PATH
    )
