from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

def create_app():
    app = Flask(__name__)
    return app

db = SQLAlchemy(model_class=Base)
