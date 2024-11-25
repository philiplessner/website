import os
import csv
from pathlib import PurePath
from typing import List
from pprint import pprint
import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select

C = os.path.abspath(os.path.dirname(__file__))
path_to_db = "".join(["sqlite:///", C, "/images.db"])
print(path_to_db)
db = sa.create_engine(path_to_db)
Session = sessionmaker(bind=db)


class Base(DeclarativeBase):
    pass


class Page(Base):
    __tablename__ = "pages_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    pagetitle: Mapped[str]
    pageroute: Mapped[str]
    images: Mapped[List["Image"]] = relationship(back_populates="pages")


class Image(Base):
    __tablename__ = "images_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    imagelink: Mapped[str]
    imagetitle: Mapped[str]
    pagerow: Mapped[int]
    pagecolumn: Mapped[int]
    page_id: Mapped[int] = mapped_column(ForeignKey("pages_table.id"))
    pages: Mapped["Page"] = relationship(back_populates="images")

    def __repr__(self) -> str:
        return f"<Image(id={self.id},imagelink={self.imagelink},imagetitle={self.imagetitle},pagerow={self.pagerow},pagecolumn={self.pagecolumn})>"


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
#    db = sa.create_engine("sqlite:///:memory:")
    main()
    csv2db("malaysia.csv")
    print_database()
    print("\n\n")