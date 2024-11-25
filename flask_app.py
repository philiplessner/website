from typing import Dict, List
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.orm import relationship
from app import create_app


class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app = create_app()
print(app.instance_path)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:////media/phil/m2ssd/web/website/images.db"
db.init_app(app)


class Page(db.Model):
    __tablename__ = "pages_table"

    id: Mapped[int] = mapped_column(primary_key=True)
    pagetitle: Mapped[str]
    pageroute: Mapped[str]
    images: Mapped[List["Image"]] = relationship(back_populates="pages")


class Image(db.Model):
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

with app.app_context():
    db.create_all()


def make_template(pagename:str) -> Dict:
    templateData = dict()
    rows = list()
    stmt = db.select(Page.pagetitle).where(Page.pagetitle==pagename)
    pname = db.session.execute(stmt)
    print(pname.scalar())
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

    '''
    templateData = {
            "title": "Ecuador",
            "rows":  [[("https://lh3.googleusercontent.com/Z1y6Uil3kQoJKEzTvnhwmQEoeFuY28woi_n-DcrtDo3mkYftjd8g_SDfndGeYZ9sLBgVMCcMGoy2F8I9qTKHAkKlq57p4xeAw-fhq7KfjEVGbkMXGkcJqavMDJembBfqNjzSGtlenA=w2400", "Glistening-green Tanager"),
            ("https://lh3.googleusercontent.com/RrnZngrB2SwNVnKlSRXNWpG-6zLjaLLrR4CrzJ5ybUNXs6ctPRtkO9e3j4SPHBVTUgaG8-VNiO5IaZvvxWRRE4cXGWa739ZqDxsoWfLIJhKErNWwMJULCn6DJTHGRNTjS6ks6j8kOQ=w2400", "Flame-faced Tanager"),
            ("https://lh3.googleusercontent.com/EDqrcjto_pCoMZDkU_CUrcTVyzNhz0KzS571gxKKxjpxz0P4Af7i9F5vK9aFUufv8vDCEIn7id7cl6kP2gomo206yNlRx44ha64nSOX4YqCq6sAcAN0kyWPvgFawyHqDm26ZPxbmIA=w2400", "Orange-Bellied Euphonia")],
            [("https://lh3.googleusercontent.com/INJL-f9jw62okmBl4G7xMZypGPgpa9Vnmcf2OQjFJ1bJZGtetzBd-RpRx6xACJ2sHBrZLpKLasGtU4JsACkwa30w_R1MxUmw1C0rbusXcPwegLkP0-uHO6c4RHld8i82aZHYAE0seQ=w2400", "Male Ecuadorian Hillstar"),
            ("https://lh3.googleusercontent.com/0DP0IeEReoODLYxg94F5cz9-N0ruXTthO8b0JEUW5pZg93Epw8lnFL_ZOSlMmYiBS6PqV0u8AU-SnYUmeVwYEGfPei54CLsgmqaPpwA_m5z_pGAHaZgDv700efSlCbf3oL4Bayd2cA=w2400", "Crowned Woodnymph"),
            ("https://lh3.googleusercontent.com/QgUvXkcvBB-QnCROv8VabSQ0h30P2eLTVc7o4rnVUN_L5yI8W7-q54okoidsTcVfqx-9Zs9jXruSo8AKUhPN4OQF396gDneT6WuiLfRQRMXTB6XZ3Qpb47nL1kRkQI4ytdxy7lSY9Q=w2400", "White-Necked Jacobin")],
            [("https://lh3.googleusercontent.com/TO8Rqj4XrmnM_fIos57yghQpX-7xl8m9NBVA90Roex9XXJQ8m4BYZUT7b2dl9c4yXPfYE50Fp_9luoj1a235USEe50bN70OCd-KCNQmXNMBI_611SjTYR7flBZNY10A3cOT-mFwYCw=w2400", "Collared Aracari"),
            ("https://lh3.googleusercontent.com/SI5bDdOoi-vbCIwnlGboq3ztA5uP9ysmOUI5tReJXefWXDu28QEIkCAbq4ZJLPE-FRcZcXqjxphRbAG6lKkyc032BsSY0ANzjY5gC859ZWUTpfcTV6LoeIBqlrDJqkOHpO8Cj2YPrA=w2400", "Andean Cock of the Rock"),
            ("https://lh3.googleusercontent.com/eHNXVNRGNcSmoyYbsR23-_NFSc33Ytz9WerY-nVL6mb84-RPVjbJemtpaNah7d-6yRoAc5T1tkd2qne6aAPmhx-vdGq7FtqEIFuTCGpTcCyljtmdpuqK7pDPjz8AFybkmuEcjffUvA=w2400", "Male Masked Trogon")],
            [("https://lh3.googleusercontent.com/g85WMHn88SJs6I_veBFL7MmlQqSH-j3F10kXbtmiUbvmH31_5fqXOcQ9DMBRqpA-x9cr_E2_33tSeJjr2gy22AORYLOngcuUZL6IH3GvzIn-AOGFxdaRvFry9h0cf-COQ928zchTGw=w2400", "Buff-Winged Starfrontlet"),
            ("https://lh3.googleusercontent.com/PJLSFsiOp63pwa5pIygGF76-vdiKGO0I_1rR8auYT0Pm5h287p4DSXPi8Fq9FqI__bjJ4Obwz0LHbTUbcjwtqqv-ezDIFK1pO1wgEUahIc9O4M9L3xQ_Clm2KNzVUDuzrnBL8p5viw=w2400", "Violet-Purple Coronet"),
            ("https://lh3.googleusercontent.com/4EQHzHkciQ5VN_U7-rBV0yGrburaafmjbytH46wbpveOvsRsrpP6SxHhrXLvXRzxtSh3ch0zPwA9H2G45wDV87F3f4pRbT03yJ4JUwnWVn9sD5cT0OKGqQhUg1fsO4VZFlYnW7apvQ=w2400", "Violet-Tailed Sylph")]]}
    '''
    templateData = make_template("Ecuador")

    return render_template('photos_template2.html', **templateData)


@app.route("/photos/brazil")
def photos_brazil():
    templateData = {
            "title": "Brazil",
            "rows":  [[("https://lh3.googleusercontent.com/pw/AP1GczNbh3-cbh9zwTBLjRC37KnWol4qL7jWnr5zmXi7AfNCgNvncbKMHeYGMx2JVu2xWpU-Ktzxs3jS4-pxKSkUYrupW1dPGg1k7aKCaSSk0L41ui57rZjBWl3o5n2DAmKKRgfjfvooaIgJ_0Sq---hSFEi=w1402-h933-s-no?authuser=0", "Male and Female Brazillian Tanager"),
            ("https://lh3.googleusercontent.com/pw/AP1GczOOidVAU7_r3prZYmTzo2yyJBaedSL7n8xDLvobduNxa4wLGPzHvUaT8jRkfh4AnGJQO5omtbwFAEvasT6nX8XguhMCOuSqq1Vi02d12txWnusScM3gEKKJgKvbVa5j4-YrLh9sOeSGIUtLgcb5_agk=w1402-h933-s-no?authuser=0", "Versicolored Emerald"),
            ("https://lh3.googleusercontent.com/pw/AP1GczOfZREyvb0K7z1qOTjWI_Vm9AyqlRF2Sym_6udZBJSoNl4hbeVxhFlDr9l947uTwJRzgVgH6_0jrCka0DnH_RCK-qm2QigLd_oCmaPrOudiNt7xcAhY0PXidUiWYMpPm_K9roW8HuTBdUEDoKqS33Qz=w1402-h933-s-no?authuser=0", "Brassy-Breasted Tanager")],
            [("https://lh3.googleusercontent.com/pw/AP1GczPQ87UT6l7OjQoXD9ZbUCb8afi6SJWHtPLUyuZ5kJqkhhWhphCZ3UyMDi6K4--HskAWkgxNRdQLC9CgEbx7iB_Ejdee_k29M9BBK1szUpw7cj-f8fX6diNrRU6lB0z_-flcRWNDZ_PQpM8Aq1HIWIaB=w1402-h933-s-no?authuser=0", "Male Chestnut-Bellied Euphonia"),
            ("https://lh3.googleusercontent.com/pw/AP1GczNyYFvsIfgPLHGE5tbyZkkZuEZlxPsSWOtUfZNcskc0w3xA2BQZYcSTmnyg0Fb-tM4jTtJWSD0KdchMbbAruPbNeq4Z-4f05OxFCioZmiY4r99Dbc748CZuL53cyy8Euid5nO8LY4PUr46bPs8Fltxc=w1401-h933-s-no?authuser=0", "Jaguar"),
            ("https://lh3.googleusercontent.com/pw/AP1GczOU8FdehKpUumF0IKQCOcJnjJYFGyXf8cnu78wDr1HqOTYS8LVVq1qYYi3x-2ajjJ3vneHbDRcMusa2MEsht6NoDlc-Vw4J4pfUHEn_b7Dwk4Nt7x3dVqWe2I96IyNMgXO8xdz2Z4KMkQtS-bFcn6TL=w1401-h933-s-no?authuser=0", "White-Tailed Hawk")],
            [("https://lh3.googleusercontent.com/pw/AP1GczM0uqnaMvI1lCbuF8SA2GFu3zPGfsTolubsg7nY0PijFGSVqIbBi6_mVUGevYGrQMbeaLd-nBqvOfiY4pyAIIJ_aB64tPjNf031f-B0VpKr25f3sIDEM8adyS5n3s6vvNtzJRXc1xrmKWNbA4MKv_yG=w1402-h933-s-no?authuser=0", "White-Throated Hummingbird"),
            ("https://lh3.googleusercontent.com/pw/AP1GczOIPbuftBsE_se58TIU-fPDp24rX3Ku6fRS9sP3FYXfydO9_oVW69v9AFcgykr9fozX2LplvO7p5C_w4WTLEvxCQ2v9VGoun9hpOWvea2jnaYgL1B1SET9nLOf-y8ntOHRAkeAeXqXxmlnLa-8hEf5L=w1402-h933-s-no?authuser=0", "Red and White Crake"),
            ("https://lh3.googleusercontent.com/pw/AP1GczN5fzhkgTCVEa_yiPnUHuPRvG0j5f2-UwElWthhpO891xRGWPSlwh2zbdIiC_OAtzy7dXsUuqK5bSXWozND_YqWLE1H1bWjKITP_Dwu-rtMYp2k9wIanWCt1tOMCT6rlmqNtLLs1BQWrQ9YP5oAjHAo=w1402-h933-s-no?authuser=0", "Male Tufted Antshrike")],
            [("https://lh3.googleusercontent.com/pw/AP1GczPi_RdOSWg0q5tYh5bG8zPfTeIVPrivG0thVY8MjrTjEgXiIG7XVSLXc2QpP_h6TlZ2Q6qRTRsL4bTEKw90mZERS8xgAqCvOWn4J1T15n41iHxCGpFvEp9DtpxCEVC_kDthh3X-MGMdaJyU1Cm_Bb2X=w1402-h933-s-no?authuser=0", "Saffron Toucanet"),
            ("https://lh3.googleusercontent.com/pw/AP1GczMFDe318RuoJ5GnajgqkNknYbGtCWJyQJwpHLCk--t3yR_rkI-oO7UxnmM07ozTi8hL2fg4-Fe7ii7OrORuiN3mb5nB25_Wr_P0mQsgyJ97DfmlsE8zfIuzYDXN_iVZQjbjc7RNCST5BonojHbGkosX=w1402-h933-s-no?authuser=0", "Black-Throated Mango"),
            ("https://lh3.googleusercontent.com/pw/AP1GczOfK1RghhaMZcVTsIkMmO-3Zirp95TcpmfkxrjPVsuASeYA-W2DwRE0W4IZ5DwyOe3VFvnNjhrbvxnaUz8G2eszLFx7hMtLwcTpsoQ-Q2w_KK73TzNqCXsaDR9HB-P_kLOf8_n31IznkyVOi66OLUk3=w1402-h933-s-no?authuser=0", "Spot-Winged Wood Quail")]]}

    return render_template('photos_template2.html', **templateData)

@app.route('/check_connection')
def check_connection():
    try:
        db.session.execute("SELECT 1")
        return "Database connection successful!"
    except Exception as e:
        return f"Database connection failed: {e}"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
