#!/bin/env python3
import sys
import os
import csv
from pprint import pprint
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Page, Image, Reference


csvfile = sys.argv[1]

def main(): 
    '''
    Connect to the images database.
    Load the load the table classes.
    Create a session.
    ***Parameters***
    None
    ***Returns***
    Session object.
    '''
    C = os.path.abspath(os.path.dirname(__file__))
    path_to_db = "".join(["sqlite:///", C, "/app/db/images.db"])
    print(path_to_db)
    db = sa.create_engine(path_to_db)
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    return Session


def csv2db(csvfile: str, Session) -> None:
    with open(csvfile, newline='') as f:
        reader = csv.DictReader(f, delimiter=',')
        rows = [row for row in reader]
    with Session() as session:
        for row in rows:
            reference = Reference(**row)
            session.add(reference)
        session.commit()


def print_database(Session) -> None:
    with Session() as session:
        stmt = (select(Reference.authors, Reference.title,
                       Reference.refinfo, Reference.reflink,
                       Reference.date, Reference.reftype)
                      .select_from(Reference)
                      )
        pprint(session.execute(stmt).all())


if __name__ == "__main__":
    Session = main()
    csv2db(csvfile, Session)
    print_database(Session)