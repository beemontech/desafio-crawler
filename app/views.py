from flask import render_template, redirect, url_for
from .celery.tasks import run_spider as spider

from .db import crawler_db


def run_spider():
    spider.delay()
    return "Spider run scheduled..."


def run_spider_in_five():
    spider.apply_async(countdown=300)
    return "Spider run scheduled to run in 5min"


def index():
    if crawler_db.db is not None:
        quotes = list(crawler_db.db.quotes.find())
        return render_template("index.html", quotes=quotes)
    return render_template("index.html")


def crear_database():
    if crawler_db.db is not None:
        crawler_db.db.quotes.drop()

    return redirect(url_for("index"))
