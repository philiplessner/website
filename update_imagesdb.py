#!/bin/env python3
import os
import csv
from pathlib import PurePath
from pprint import pprint
import click
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Page, Image


@click.command()
@click.option('-f', 'csvfile')
@click.option('-d', 'dbfile')
def csv2db(csvfile: str, dbfile: str ) -> None:
    '''
    Update the Images and Pages table in database from a CSV file.
    Name of CSV file is name of photos page (lower case).
    Each row of CSV file is: imagelink, imagetitle, imagerow, imagecolumn.
    A list of dicts is created from the rows of the CSV file:
    [{"imagelink":imagelink, "imagetitle":imagetitle, "pagerow":pagerow, "pagecolumn":pagecolumn},...]
    A dict is created to hold the page information:
    {"pagetitle":title, "pageroute":route}
    ***Parameters***
    csvfile: path to csvfile
    dbfile: name of db file (stored in app/db directory) or "memory" to use an in-memory database for testing
    ***Returns***
    None
    '''
    if (dbfile == 'memory'):
        db = sa.create_engine("sqlite://")
        print("The database is an in-memory database")
    else:
        path2this_directory = os.path.abspath(os.path.dirname(__file__))
        path2db = f"sqlite:///{os.path.join(path2this_directory, 'app/db',dbfile)}"
        print(f"The database is located at: {path2db}")
        db = sa.create_engine(path2db)
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
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
        stmt = select(Page.id).where(Page.pagetitle==pagedict["pagetitle"])
        result = session.scalar(stmt)  # Returns None if page is not in database
        print(f"The Page id is: {result}")
        if (not result):
            page = Page(**pagedict)
            session.add(page)
            session.commit()
            stmt = select(Page).order_by(Page.id.desc()).limit(1)
            print(f"The new Page Record is: {session.execute(stmt).all()}")
            for row in rows:
                image = Image(**row)
                image.pages = page
                session.add(image)
        else:
            page = result
            for row in rows:
                row.update({"page_id": page})
                image = Image(**row)
                session.add(image)

        session.commit()
        stmt = select(Image).order_by(Image.id.desc()).limit(len(rows))
        pprint(session.execute(stmt).all())


if __name__ == "__main__":
    csv2db()