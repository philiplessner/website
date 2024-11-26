import sys
import os
import csv
from pathlib import PurePath
from pprint import pprint
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Page, Image


C = os.path.abspath(os.path.dirname(__file__))
path_to_db = "".join(["sqlite:///", C, "/app/db/images.db"])
print(path_to_db)
db = sa.create_engine(path_to_db)
Session = sessionmaker(bind=db)
csvfile = sys.argv[1]


def main() -> None:
    Base.metadata.create_all(db)


def csv2db(csvfile: str) -> None:
    rows = list()
    pagedict = dict()
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            row["pagerow"] = int(row["pagerow"])
            row["pagecolumn"] = int(row["pagecolumn"])
            rows.append(row)

    p = PurePath(csvfile)
    title = p.stem.capitalize()
    route = "".join(["/photos/",p.stem])
    pagedict.update({"pagetitle": title, "pageroute": route})

    with Session() as session:
        page = Page(**pagedict)
        session.add(page)
        session.commit()
        for row in rows:
            image = Image(**row)
            image.pages = page
            session.add(image)
        session.commit()


def print_database() -> None:
    with Session() as session:
        stmt = (select(Image.imagelink, Image.imagetitle,
                      Image.pagerow, Image.pagecolumn,
                      Image.page_id, Page.pagetitle)
                      .select_from(Image)
                      .join(Page, Image.page_id==Page.id))
        pprint(session.execute(stmt).all())


if __name__ == "__main__":
    main()
    csv2db(csvfile)
    print_database()