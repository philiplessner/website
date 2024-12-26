import os
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    app = create_app()
    path2this_directory = os.path.abspath(os.path.dirname(__file__))
    path2parent_directory = os.path.abspath(os.path.join(path2this_directory, os.pardir))
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{os.path.join(path2parent_directory, 'app/db/website.db')}"
    })
    db.init_app(app)
    with app.app_context():
        db.create_all()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client