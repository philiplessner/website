import os
from app import app, db

# We need to get this path to find the file. It will be different on the development and production server.
path2this_directory = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "".join(["sqlite:///", path2this_directory, "/app/db/website.db"])
db.init_app(app)
with app.app_context():
    db.create_all()


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
