import os
import yaml
import click
from pprint import pprint
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select
from app.models import Base, Blog


@click.command()
@click.option('-f', 'filename')
def update(filename):
    '''
    Update a blog entry or create a record with a new blog entry.
    Reads from three files:
    filename_body.html: Contains the body of the post.
    filename_abstract.html: Contains the abstract of the post.
    filename.yaml: Contains the following fields:
    id: The primary key id. If this is a new blog post, set it to a negative number.
    title
    date
    medialink
    mediatype
    path2abstract: Path to the filename_abstract.html file
    path2body: Path to the filename_body.html file
    '''
    C = os.path.abspath(os.path.dirname(__file__))
    path_to_db = "".join(["sqlite:///", C, "/app/db/website.db"])
    db = sa.create_engine(path_to_db)
    Base.metadata.create_all(db)
    yaml_file = "".join([filename, ".yaml"]) 
    print(yaml_file)
    with open(yaml_file, "r") as f:
        data = yaml.safe_load(f)
    body_file = data['path2body']
    with open(body_file, "r") as f:
        body = f.read()
    data.update({"body": body})
    data.pop("path2body")
    abstract_file =data["path2abstract"]
    with open(abstract_file, "r") as f:
        abstract = f.read()
    data.update({"abstract": abstract})
    data.pop("path2abstract")
    pprint(data)
    Session = sessionmaker(bind=db)
    with Session() as session:
        if (data['id'] >= 0):
            stmt = select(Blog).where(Blog.id==data['id'])
            record = session.execute(stmt).scalar_one()
            print(record)
            record.title = data['title']
            record.date = data['date']
            record.medialink = data['medialink']
            record.mediatype = data['mediatype']
            record.abstract = data['abstract']
            record.body = data['body']
            record.pagecss = data.get('pagecss', None)
        else:
            data.pop("id")
            record = Blog(**data)
            session.add(record)
        session.commit()

if __name__ == "__main__":
    update()
