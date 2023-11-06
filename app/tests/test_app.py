import os
from flask import Flask
from app.app import app, celery_app


def test_app_creation():
    assert isinstance(app, Flask)


def test_celery_app():
    assert celery_app is not None


def test_app_routes():
    assert "index" in app.view_functions
    assert "run_spider" in app.view_functions
    assert "run_spider_in_five" in app.view_functions
