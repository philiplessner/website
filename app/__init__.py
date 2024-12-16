from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from app.models import Base

app = Flask(__name__)
db = SQLAlchemy(model_class=Base)
from app import routes, models

