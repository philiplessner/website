from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

db = SQLAlchemy(model_class=Base)


def create_app():
    app = Flask(__name__)
    from app import routes, models
    app.register_blueprint(routes.bp)
    return app
