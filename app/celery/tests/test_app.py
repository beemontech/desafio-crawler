import os
from flask import Flask
from app.celery.app import make_celery


def test_make_celery():
    app = Flask(__name__)
    app.config["CELERY"] = {
        "broker_url": os.environ["REDIS_URI"],
        "result_backend": os.environ["REDIS_URI"],
        "always_eager": True,  # Run tasks local
    }

    celery = make_celery(app)

    assert celery.conf.broker_url == app.config["CELERY"]["broker_url"]
    assert celery.conf.result_backend == app.config["CELERY"]["result_backend"]
    assert celery.conf.always_eager == app.config["CELERY"]["always_eager"]
