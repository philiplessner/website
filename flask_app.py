from flask import Flask, render_template
import datetime


app = Flask(__name__)


@app.route("/")
def hello():
    now = datetime.datetime.now()
    timeString = now.strftime("%Y-%m-%d %H:%M")
    templateData = {
            'title': 'Home',
            'time': timeString
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
    templateData = {
            "title": "Ecuador",
            "row1":  [("https://lh3.googleusercontent.com/Z1y6Uil3kQoJKEzTvnhwmQEoeFuY28woi_n-DcrtDo3mkYftjd8g_SDfndGeYZ9sLBgVMCcMGoy2F8I9qTKHAkKlq57p4xeAw-fhq7KfjEVGbkMXGkcJqavMDJembBfqNjzSGtlenA=w2400", "Glistening-green Tanager"),
            ("https://lh3.googleusercontent.com/RrnZngrB2SwNVnKlSRXNWpG-6zLjaLLrR4CrzJ5ybUNXs6ctPRtkO9e3j4SPHBVTUgaG8-VNiO5IaZvvxWRRE4cXGWa739ZqDxsoWfLIJhKErNWwMJULCn6DJTHGRNTjS6ks6j8kOQ=w2400", "Flame-faced Tanager"),
            ("https://lh3.googleusercontent.com/EDqrcjto_pCoMZDkU_CUrcTVyzNhz0KzS571gxKKxjpxz0P4Af7i9F5vK9aFUufv8vDCEIn7id7cl6kP2gomo206yNlRx44ha64nSOX4YqCq6sAcAN0kyWPvgFawyHqDm26ZPxbmIA=w2400", "A Tanager")],
            "row2":  [("https://lh3.googleusercontent.com/INJL-f9jw62okmBl4G7xMZypGPgpa9Vnmcf2OQjFJ1bJZGtetzBd-RpRx6xACJ2sHBrZLpKLasGtU4JsACkwa30w_R1MxUmw1C0rbusXcPwegLkP0-uHO6c4RHld8i82aZHYAE0seQ=w2400", "Male Ecuadorian Hillstar"),
            ("https://lh3.googleusercontent.com/0DP0IeEReoODLYxg94F5cz9-N0ruXTthO8b0JEUW5pZg93Epw8lnFL_ZOSlMmYiBS6PqV0u8AU-SnYUmeVwYEGfPei54CLsgmqaPpwA_m5z_pGAHaZgDv700efSlCbf3oL4Bayd2cA=w2400", "A Hummingbird"),
            ("https://lh3.googleusercontent.com/QgUvXkcvBB-QnCROv8VabSQ0h30P2eLTVc7o4rnVUN_L5yI8W7-q54okoidsTcVfqx-9Zs9jXruSo8AKUhPN4OQF396gDneT6WuiLfRQRMXTB6XZ3Qpb47nL1kRkQI4ytdxy7lSY9Q=w2400", "A Hummingbird")],
            "row3":  [("https://lh3.googleusercontent.com/TO8Rqj4XrmnM_fIos57yghQpX-7xl8m9NBVA90Roex9XXJQ8m4BYZUT7b2dl9c4yXPfYE50Fp_9luoj1a235USEe50bN70OCd-KCNQmXNMBI_611SjTYR7flBZNY10A3cOT-mFwYCw=w2400", "Collared Aracari"),
            ("https://lh3.googleusercontent.com/SI5bDdOoi-vbCIwnlGboq3ztA5uP9ysmOUI5tReJXefWXDu28QEIkCAbq4ZJLPE-FRcZcXqjxphRbAG6lKkyc032BsSY0ANzjY5gC859ZWUTpfcTV6LoeIBqlrDJqkOHpO8Cj2YPrA=w2400", "Andean Cock of the Rock"),
            ("https://lh3.googleusercontent.com/eHNXVNRGNcSmoyYbsR23-_NFSc33Ytz9WerY-nVL6mb84-RPVjbJemtpaNah7d-6yRoAc5T1tkd2qne6aAPmhx-vdGq7FtqEIFuTCGpTcCyljtmdpuqK7pDPjz8AFybkmuEcjffUvA=w2400", "Male Masked Trogon")],
            "row4":  [("https://lh3.googleusercontent.com/g85WMHn88SJs6I_veBFL7MmlQqSH-j3F10kXbtmiUbvmH31_5fqXOcQ9DMBRqpA-x9cr_E2_33tSeJjr2gy22AORYLOngcuUZL6IH3GvzIn-AOGFxdaRvFry9h0cf-COQ928zchTGw=w2400", "A Hummingbird"),
            ("https://lh3.googleusercontent.com/PJLSFsiOp63pwa5pIygGF76-vdiKGO0I_1rR8auYT0Pm5h287p4DSXPi8Fq9FqI__bjJ4Obwz0LHbTUbcjwtqqv-ezDIFK1pO1wgEUahIc9O4M9L3xQ_Clm2KNzVUDuzrnBL8p5viw=w2400", "A Hummingbird"),
            ("https://lh3.googleusercontent.com/4EQHzHkciQ5VN_U7-rBV0yGrburaafmjbytH46wbpveOvsRsrpP6SxHhrXLvXRzxtSh3ch0zPwA9H2G45wDV87F3f4pRbT03yJ4JUwnWVn9sD5cT0OKGqQhUg1fsO4VZFlYnW7apvQ=w2400", "A Hummingbird")]}

    return render_template('photos_ecuador.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
