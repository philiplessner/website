import click
import os
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Blog


@click.command()
@click.option('-f', 'filename')
@click.option('-i', 'blogid', type=int)
def db2file(filename, blogid):
    C = os.path.abspath(os.path.dirname(__file__))
    path_to_db = "".join(["sqlite:///", C, "/app/db/website.db"])
    db = sa.create_engine(path_to_db)
    Base.metadata.create_all(db)
    Session = sessionmaker(bind=db)
    with Session() as session:
        stmt = (select(Blog.body,
                       Blog.title,
                       Blog.abstract,
                       Blog.date,
                       Blog.medialink,
                       Blog.mediatype
                       )
                      .select_from(Blog)
                      .where(Blog.id==blogid)
                      )
        body = session.execute(stmt).all()[0][0]
    with open("".join([filename, ".html"]), "w", encoding="utf-8") as f:
        f.write(body)



if __name__ == "__main__":
    db2file()