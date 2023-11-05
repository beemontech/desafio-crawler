import os
from .celery.app import make_celery
from flask import Flask
from flask_pymongo import PyMongo
from . import views

CRAWLER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "crawler")

app = Flask(__name__)
app.config["MONGO_URI"] = os.environ["MONGODB_URI"]
mongo = PyMongo(app)
db = mongo.db

# celery config
app.config.from_mapping(
    CELERY=dict(
        broker_url="redis://redis:6379/0", result_backend="redis://redis:6379/0"
    )
)

celery_app = make_celery(app)

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/run_spider", view_func=views.run_spider, methods=["POST"])
