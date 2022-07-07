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
def photos():
    templateData = {
            'title': 'Ecuador'
            }
    return render_template('photos_ecuador.html', **templateData)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)
