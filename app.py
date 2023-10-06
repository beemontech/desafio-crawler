import pymongo

from decouple import config
from flask import Flask, current_app

app = Flask(__name__)


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        MONGODB_COLLECTION=config("MONGODB_COLLECTION"),
        MONGODB_URI=config("MONGODB_URI"),
        MONGODB_DB=config("MONGODB_DB"),
    )
    @app.route("/")
    def home():
        collection_name = current_app.config["MONGODB_COLLECTION"]
        client = pymongo.MongoClient(current_app.config["MONGODB_URI"])
        db = client[current_app.config["MONGODB_DB"]]
        movies_collection = db[collection_name]

        html = ""
        for move in movies_collection.find():
            html += "<div style='margin-top:5px;padding:5px 0 0 0'>"
            html += "<p><b>ID:</b> {}</p>".format(str(move["_id"]))
            html += "<p><b>Position:</b> {}</p>".format(move["position"])
            html += "<p><b>Name:</b> {}</p>".format(move["name"])
            html += "<p><b>Year:</b> {}</p>".format(move["year"])
            html += "<p><b>Duration:</b> {}</p>".format(move["duration"])
            html += "<p><b>Rating:</b> {}</p>".format(move["rating"])
            html += (
                "<p><a href='{}' title='click to see more' target='_blank'><img src='{}'></a></p>".format(
                    move["link"], move["image"]
                )
            )
            html += "<hr>"
            html += "</div>"

        if not html:
            html += "<p>Sorry, we're empty. Please, run the crawler first (<i>the README file has the instructions</i>).</p>"
        return html

    return app
