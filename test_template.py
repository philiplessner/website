from typing import Dict, Union, List
from datetime import date
from collections import namedtuple
from pprint import pprint
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import app
from app.models import Base, Page, Image, Reference


def about_me_template2():
    References = namedtuple('References', ['authors', 'title', 'reference', 'date', 'link', 'type'])
    references = dict()
    stmt = (db.select(Reference.authors, Reference.title,
                      Reference.refinfo, Reference.date,
                      Reference.reflink, Reference.reftype)
                      .select_from(Reference)
                      .where(Reference.reftype == "Paper"))
    papers = [References(*row) for row in db.session.execute(stmt).all()]
    stmt = (db.select(Reference.authors, Reference.title,
                      Reference.refinfo, Reference.date,
                      Reference.reflink, Reference.reftype)
                      .select_from(Reference)
                      .where(Reference.reftype == "Patent"))
    patents= [References(*row) for row in db.session.execute(stmt).all()]
    for ref in patents:
        print(date.fromisoformat(ref.date))

    print(list(map(lambda x: x[3], patents)))
    patents = sorted(patents, key=lambda x: x[3], reverse=True)
    print(patents) 
    references.update({"papers": papers, "patents": patents})
#    pprint(references)


db = SQLAlchemy(model_class=Base)
# We need to get this path to find the file. It will be different on the development and production server.
path2this_directory = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "".join(["sqlite:///", path2this_directory, "/app/db/website.db"])
db.init_app(app)
with app.app_context():
    db.create_all()
    about_me_template2()

