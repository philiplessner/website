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
    '''
    Get a blog post from database. Three files are created:
    filename_body.html: The body of the post
    filename_abstract.html: The abstract of the post
    filename.yaml: Contains the other fields in the database record plus the path to the body and abstract files
    These files will be read by update_blogs.py to update the post in the database.
    '''
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
                       Blog.mediatype,
                       Blog.id,
                       Blog.pagecss
                       )
                      .select_from(Blog)
                      .where(Blog.id==blogid)
                      )
        result = session.execute(stmt).all()
        body = result[0][0]
        title = result[0][1]
        abstract =result[0][2]
        date = result[0][3]
        medialink = result[0][4]
        mediatype = result[0][5]
        id = result[0][6]
        pagecss = result[0][7]
        yaml = "".join(["id: ", str(id), "\n", 
                        "title: '", title, "'\n",
                        "date: '", date, "'\n",
                        "medialink: '", medialink, "'\n",
                        "mediatype: '", mediatype, "'\n",
                        "path2abstract: '", C, "/", filename, "_abstract.html'\n",
                        "path2body: '", C, "/", filename, "_body.html'", ])
    with open("".join([filename, "_body.html"]), "w", encoding="utf-8") as f:
        f.write(body)
    with open("".join([filename, "_abstract.html"]), "w", encoding="utf-8") as f:
        f.write(abstract)
    with open("".join([filename, ".yaml"]), "w", encoding="utf-8") as f:
        f.write("".join([yaml, "\npagecss: '", pagecss, "'"]) if pagecss else yaml)



if __name__ == "__main__":
    db2file()