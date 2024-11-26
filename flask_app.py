from typing import Dict
import os
from flask import render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from app import app
from app.models import Base, Page, Image


db = SQLAlchemy(model_class=Base)
C = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "".join(["sqlite:///", C, "/app/db/images.db"])
db.init_app(app)
with app.app_context():
    db.create_all()


def make_template(pagename:str) -> Dict:
    templateData = dict()
    rows = list()
    stmt = db.select(Page.pagetitle).where(Page.pagetitle==pagename)
    #db.session.execute(stmt)
    templateData.update({"title": db.first_or_404(stmt)})
    stmt = db.select(func.max(Image.pagerow)).join(Page).where(Page.pagetitle==pagename)
    maxrows = db.session.execute(stmt).all()[0][0]
    for i in range(maxrows+1):
        stmt = (db.select(Image.imagelink, Image.imagetitle)
                .select_from(Image)
                .join(Page, Image.page_id==Page.id)
                .where(Page.pagetitle==pagename)
                .where(Image.pagerow==i))
        rows.append(db.session.execute(stmt).all())
    templateData.update({"rows": rows})
    return templateData


@app.route("/")
def hello():
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


@app.route("/aboutme")
def about_me():
    templateData = {
            'title': 'About'
            }
    return render_template('about_me.html', **templateData)


@app.route("/photos/ecuador")
def photos_ecuador():
    templateData = make_template("Ecuador")
    return render_template('photos_template2.html', **templateData)


@app.route("/photos/brazil")
def photos_brazil():
    templateData = make_template("Brazil")
    return render_template('photos_template2.html', **templateData)


@app.route("/photos/malaysia")
def photos_malaysia():
    templateData = make_template("Malaysia")
    return render_template('photos_template2.html', **templateData)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
