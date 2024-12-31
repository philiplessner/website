#!/bin/env python3
import os
import csv
from pprint import pprint
import click
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Reference


@click.command()
@click.option('-f', 'csvfile')
@click.option('-d', 'dbfile')
def csv2db(csvfile: str, dbfile: str) -> None:
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
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = [row for row in reader]
    with Session() as session:
        for row in rows:
            reference = Reference(**row)
            session.add(reference)
        session.commit()
        stmt = select(Reference).order_by(Reference.id.desc()).limit(len(rows))
        pprint(session.execute(stmt).all())


if __name__ == "__main__":
    csv2db()