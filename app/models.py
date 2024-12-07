from typing import List
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship


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
    

class Reference(Base):
    __tablename__ = "references_table"
    id: Mapped[int] = mapped_column(primary_key=True)
    authors: Mapped[str]
    title: Mapped[str]
    refinfo: Mapped[str]
    date: Mapped[str]
    reflink: Mapped[str]
    reftype: Mapped[str]
        
