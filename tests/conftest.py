import os
import pytest
from app import create_app, db

@pytest.fixture(scope='module')
def test_client():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    path2this_directory = os.path.abspath(os.path.dirname(__file__))
    path2parent_directory = os.path.abspath(os.path.join(path2this_directory, os.pardir))
    app.config["SQLALCHEMY_DATABASE_URI"] = "".join(["sqlite:///", path2parent_directory,  "/app/db/website.db"])
    db.init_app(app)
    with app.app_context():
        db.create_all()
    with app.test_client() as testing_client:
        with app.app_context():
            yield testing_client