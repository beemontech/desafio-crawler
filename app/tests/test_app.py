import os
from flask import Flask
from app.app import app, mongo, celery_app


def test_app_creation():
    assert isinstance(app, Flask)


def test_mongo_connection():
    assert mongo.cx is not None


def test_celery_app():
    assert celery_app is not None


def test_app_routes():
    assert "index" in app.view_functions
    assert "run_spider" in app.view_functions
