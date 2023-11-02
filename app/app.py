import os
import subprocess
from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo

CRAWLER_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'crawler')

def setup_app():
    app = Flask(__name__)
    app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
    mongo = PyMongo(app)
    db = mongo.db

    @app.route('/run_spider', methods=['POST'])
    def run_spider():
        spider_name = 'quotes'
        subprocess.check_output(['scrapy', 'crawl', spider_name, '-o', 'quotes-subprocess.json'], cwd=CRAWLER_PATH)
        return "Spider run successfully"

    @app.route('/')
    def index():
        return render_template('index.html')
    return app