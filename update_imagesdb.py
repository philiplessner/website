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
def csv2db(csvfile: str ) -> None:
    '''
    Update the website database from a CSV file.
    Name of CSV file is name of photos page (lower case).
    Each row of CSV file is: imagelink, imagetitle, imagerow, imagecolumn.
    A list of dicts is created from the rows of the CSV file:
    [{"imagelink":imagelink, "imagetitle":imagetitle, "pagerow":pagerow, "pagecolumn":pagecolumn},...]
    A dict is created to hold the page information:
    {"pagetitle":title, "pageroute":route}
    ***Parameters***
    csvfile: path to csvfile
    Session: Session object created in main()
    ***Returns***
    None
    '''
    path2this_directory = os.path.abspath(os.path.dirname(__file__))
    path2db = f"sqlite:///{os.path.join(path2this_directory, 'app/db/website.db')}"
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
            print(page)
            session.add(page)
            session.commit()
            for row in rows:
                image = Image(**row)
                image.pages = page
                session.add(image)
        else:
            stmt = select(Page.id).where(Page.pagetitle==pagedict["pagetitle"])
            page = session.execute(stmt).scalar()
            print(page)
            for row in rows:
                row.update({"page_id": page})
                image = Image(**row)
                session.add(image)

        session.commit()



if __name__ == "__main__":
    csv2db()