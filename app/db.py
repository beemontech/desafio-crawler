from flask_pymongo import PyMongo
import os

crawler_db = PyMongo()


def init_db(app):
    app.config[
        "MONGO_URI"
    ] = f'{os.environ["MONGODB_URI"]}/{os.environ["MONGO_DATABASE"]}'
    crawler_db.init_app(app)
