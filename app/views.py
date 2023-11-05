from flask import render_template
from .celery.tasks import run_spider as spider


def run_spider():
    spider.delay()
    return "Spider run scheduled..."


def index():
    return render_template("index.html")
