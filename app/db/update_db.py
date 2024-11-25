import csv
from pathlib import PurePath
from typing import Dict, List
from pprint import pprint
import sqlalchemy as sa
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, sessionmaker, DeclarativeBase
from sqlalchemy.orm import relationship
from sqlalchemy.sql import select

db = sa.create_engine("sqlite:///images.db")
#db = sa.create_engine("mysql+mysqldb://root:blueskyMorning1!@localhost:3306/msql-images.db")
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

def add_data(pagedata:dict, pageurl:str) -> None:
    with Session() as session:
        page = Page(pagetitle=pagedata["title"], pageroute=pageurl)
        session.add(page)
        session.commit()
        for i, row in enumerate(pagedata["rows"]):
            for j, column in enumerate(row):
                imagelink =column[0]
                imagetitle = column[1]
                image = Image(imagelink=imagelink, imagetitle=imagetitle,
                              pagerow=i, pagecolumn=j)
                image.pages = page
                session.add(image)
        session.commit()


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



def make_template(pagename:str) -> Dict:
    templateData = dict()
    rows = list()
    with Session() as session:
        stmt =select(Page.pagetitle).where(Page.pagetitle==pagename)
        templateData.update({"title": session.execute(stmt).first()[0]})
        stmt = select(func.max(Image.pagerow)).join(Page).where(Page.pagetitle==pagename)
        maxrows = session.execute(stmt).all()[0][0]
        for i in range(maxrows+1):
            stmt = (select(Image.imagelink, Image.imagetitle)
                    .select_from(Image)
                    .join(Page, Image.page_id==Page.id)
                    .where(Page.pagetitle==pagename)
                    .where(Image.pagerow==i))
            rows.append(session.execute(stmt).all())
    templateData.update({"rows": rows})
    return templateData


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
    csv2db("ecuador.csv")
    csv2db("brazil.csv")
    #add_data(ecuador, "/photos/ecuador")
    #add_data(brazil, "photos/brazil")
    print_database()
    print("\n\n")
    template = make_template("Ecuador")
    pprint(template)
    print("\n\n")
    template = make_template("Brazil")
    pprint(template)