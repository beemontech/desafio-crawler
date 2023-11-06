from contextlib import contextmanager
from flask import template_rendered
from app.app import app
import pytest


@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_run_spider(client):
    rv = client.post("/run_spider")
    assert rv.status_code == 200
    assert b"Spider run scheduled..." in rv.data


def test_index(client):
    with captured_templates(app) as templates:
        rv = client.get("/")
        assert rv.status_code == 200
        template, _ = templates[0]
        assert template.name == "index.html"
