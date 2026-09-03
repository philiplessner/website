import os
import sqlite3

import pytest

from app import create_app, db


@pytest.fixture
def test_app():
    app = create_app()
    path2this_directory = os.path.abspath(os.path.dirname(__file__))
    path2parent_directory = os.path.abspath(os.path.join(path2this_directory, os.pardir))
    database_path = os.path.join(path2parent_directory, 'app/db/website.db')
    app.config.update({
        "TESTING": True,
        "WTF_CSRF_ENABLED": False,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:"
    })
    db.init_app(app)
    with app.app_context():
        destination = db.engine.raw_connection()
        try:
            with sqlite3.connect(database_path) as source:
                source.backup(destination.driver_connection)
        finally:
            destination.close()
    yield app


@pytest.fixture
def test_database(test_app):
    with test_app.app_context():
        yield db


@pytest.fixture
def test_client(test_app):
    with test_app.test_client() as testing_client:
        yield testing_client
