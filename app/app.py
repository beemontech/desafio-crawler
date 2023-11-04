import os
from .celery.app import make_celery
from flask import Flask
from flask_pymongo import PyMongo

CRAWLER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crawler')

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
mongo = PyMongo(app)
db = mongo.db

# celery config
app.config.from_mapping(
    CELERY=dict(
        broker_url='redis://redis:6379/0',
        result_backend='redis://redis:6379/0'
    )
)

celery_app = make_celery(app)

from . import views
app.add_url_rule('/', view_func=views.index)
app.add_url_rule('/run_spider', view_func=views.run_spider, methods=["POST"])
