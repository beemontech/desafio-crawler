import os
from .celery.app import make_celery
from flask import Flask
from flask_pymongo import PyMongo
from . import views, db

app = Flask(__name__)

db.init_db(app)

# celery config
app.config.from_mapping(
    CELERY=dict(
        broker_url=os.environ["REDIS_URI"], result_backend=os.environ["REDIS_URI"]
    )
)
celery_app = make_celery(app)

app.add_url_rule("/", view_func=views.index)
app.add_url_rule("/run_spider", view_func=views.run_spider, methods=["POST"])
app.add_url_rule(
    "/run_spider_in_five", view_func=views.run_spider_in_five, methods=["POST"]
)
app.add_url_rule("/clear_database", view_func=views.crear_database, methods=["POST"])
