from collections import namedtuple
from flask import render_template, send_from_directory
from sqlalchemy import func
from app import db
from app.models import Page, Image, Reference, Blog
from flask import Blueprint

bp = Blueprint('views', __name__, url_prefix='/')

@bp.route("/")
def home():
    templateData = {
            'title': 'Home',
            "imageData":  [("https://lh3.googleusercontent.com/a0b8trXwHAZyZldHkDL7quh3nk2A10EjCddB-RWvuo0zpyUYXz38ANTizqLbtpT-oio4Rc9QjByCdPJYVcKFWsyyn8kHbqu0sn_7BiU-D_s55OjbVXuAEC87vCVIZaMpYBPdiUqFjw=w2400", "Jaguar in the Brazilian Pantanal"),
            ("https://lh3.googleusercontent.com/NrLffcEzJRV0sOWA9zRSyWZI5pZ1fyHpjV6k8_tnNO64ZSOLT5UFfQI-LAcAqctBdQFWaC4YO6u1VTopGLbzAcz9BIW5fHx8dk_Pdlhw6RzgZEjBq_TFZPP7yvz_hZfEd1wTZeGF8Q=w2400", "Chimpanzee in Buhoma sector of Bwindi Impenetrable Forest NP, Uganda"),
            ("https://lh3.googleusercontent.com/dprFHYMozoatjaa7zXdMKRNhRd6eCasVJIvo62dmqx-DrxuDRCzkNTTNZEyW-ch47AGydo7Dvmp-gLWy68KAdc8o7dBLEQ2OoGWs_XZRcuzLZ54_k3T7G0XdxY5y62Fhlh2c62sMAA=w2400", "Asian Crested Ibis at Yangxian, China"),
            ("https://lh3.googleusercontent.com/fmZwOR53opkwq4FtvNcUrxp4Ek9pmMRKVMkAOpJj8Jp9uRO7A4LlPQ7C8mr_qVAtYv06llXOaxr5vb5SO6nJCa_zc8xxrglYPxXWDn6BTf7tSFwNpFlh8EK_8o1T7_rt3Erou3iNhA=w2400", "Collared Aracari at Mirador Los Bancos, Ecuador"),
            ("https://lh3.googleusercontent.com/EbApyLkB3SDXerEJpGCBpfsvdHvap3ePTZ7JfXmcaLoiCvTo_JSdk0ZaxH-oGP1PeqV31ssSv7N-Qyw8DYV8k-NBhQmD6eZynuAxT_TVdBzRCtnDAo8t2d9QkIvtljaICKRzx4aXrg=w2400", "Pont Du Gard, France"),
            ("https://lh3.googleusercontent.com/lfe96RR_ewnAyNWwVOafeuD4PU88U3FOt-xCdYVVM3Jz_YIgmWvCeDzMDWCCOsR7UpfXi6RUVzpAYuHXyAzJHf0srbclVM7Z9UektDht6faBnwgwzE3KMXyXxPpdDHAYn7EEGpW5rw=w2400", "Fire-tufted Barbet at Bukit Fraser, Malyasia"),
            ("https://lh3.googleusercontent.com/BSZCcP7yCA28fXsAlVaL0xg7BmHGknBqfT2qDDi8x6zCtadnuRgdM7xylHaiwOGM0QWiDlJRJonCw0LnUFUcQBAqlMwAuu60zLoAxfH-867jzPYMKmR0CLS-4Xd4eGExdvvI245m7w=w2400", "Frigatebird in Galapagos")]
            }
    return render_template('index.html', **templateData)


@bp.route("/blog")
def blog():
    stmt = (db.select(Blog.title, Blog.abstract, Blog.date, Blog.medialink, Blog.mediatype, Blog.id)
                      .select_from(Blog)
                      .order_by(Blog.date.desc()))
    blogs = db.session.execute(stmt).all()
    rows = list()
    row = list()
    count = 0
    for blog in blogs:
        row.append(blog)
        count = count + 1
        if ((count == 2) or (blog == blogs[-1])):
            rows.append(row)
            row = []
            count = 0
    templateData = {"rows": rows}
    templateData['title'] = "Blog"
    return render_template('blog.html', **templateData)


@bp.route("/blog/<blogid>")
def blogpost(blogid):
    Post  = namedtuple('Post', ['title', 'body', 'date', 'id', 'pagecss'])
    stmt = (db.select(Blog.title, Blog.body, Blog.date, Blog.id, Blog.pagecss)
                      .select_from(Blog)
                      .where(Blog.id == blogid))
    blog = Post(*(db.session.execute(stmt).all()[0]))
    templateData = {"blogdata": blog}
    templateData['title'] = "Blog"
    return render_template('blogpost.html', **templateData)


@bp.route("/photos/<location>")
def photos(location):
    '''
    cap_location(str): Page Name (first letter should be capitalized). This is used to look up
                    the entries in a sqlite database.
    Dictionary for template of form {title:pagename, 
                                     rows:[[(imagelink, imagetitle ), ...], [(imagelink, imagetitle), ...]]}
    Each entry is a tuple. Each row is a list of tuples. The complete structure is a list of lists.
    '''
    cap_location = location.capitalize()
    templateData = dict()
    rows = list()
    stmt = db.select(Page.pagetitle).where(Page.pagetitle==cap_location)
    templateData.update({"title": db.first_or_404(stmt)})
    stmt = db.select(func.max(Image.pagerow)).join(Page).where(Page.pagetitle==cap_location)
    maxrows = db.session.scalar(stmt)
    for i in range(maxrows+1):
        stmt = (db.select(Image.imagelink, Image.imagetitle)
                .select_from(Image)
                .join(Page, Image.page_id==Page.id)
                .where(Page.pagetitle==cap_location)
                .where(Image.pagerow==i))
        rows.append(db.session.execute(stmt).all())
    templateData.update({"rows": rows})
    return render_template('photos_template.html', **templateData)


@bp.route("/aboutme")
def about_me():
    templateData = {'title': 'About'}
    References = namedtuple('References', ['authors', 'title', 'reference', 'date', 'link', 'type'])
    references = dict()
    stmt = (db.select(Reference.authors, Reference.title,
                      Reference.refinfo, Reference.date,
                      Reference.reflink, Reference.reftype)
                      .select_from(Reference)
                      .where(Reference.reftype == "Paper")
                      .order_by(Reference.date.desc()))
    papers = [References(*row) for row in db.session.execute(stmt).all()]
    stmt = (db.select(Reference.authors, Reference.title,
                      Reference.refinfo, Reference.date,
                      Reference.reflink, Reference.reftype)
                      .select_from(Reference)
                      .where(Reference.reftype == "Patent")
                      .order_by(Reference.date.desc()))
    patents= [References(*row) for row in db.session.execute(stmt).all()]
    stmt = (db.select(Reference.authors, Reference.title,
                      Reference.refinfo, Reference.date,
                      Reference.reflink, Reference.reftype)
                      .select_from(Reference)
                      .where(Reference.reftype == "Presentation")
                      .order_by(Reference.date.desc()))
    presentations = [References(*row) for row in db.session.execute(stmt).all()]
    references.update({"papers": papers, "patents": patents, "presentations": presentations})
    templateData.update(references)
    return render_template('about_me.html', **templateData)

@bp.route("/resume/<path:filename>")
def download_resume(filename):
    return(send_from_directory("files", filename))

