from flask import Flask, redirect, render_template, request, url_for
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import os

# Get path
basedir = os.path.abspath(os.path.dirname(__file__))


# Initialize app
app = Flask(__name__)

# Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

# Register package to the app
moment = Moment(app)
db = SQLAlchemy(app)
bootstrap = Bootstrap5(app)


# Create Tabel Pengeraman
class Pengeraman(db.Model):
    id = db.Column("pengeraman_id", db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    # def __init__(self):
    #     pass

    def __repr__(self):
        return "<Name {}>".format(self.name)


# Router
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form["start"] == "start":  # Get button start
            data = Pengeraman(name="Telur Ayam", created_at=datetime.utcnow())
            db.session.add(data)  # add data
            db.session.commit()  # push data to database
            return redirect(url_for("start"))
    return render_template("pages/index.html", title="Start")


@app.route("/start")
def start():
    first_light = True
    return render_template(
        "pages/pengeraman.html", title="Proses Pengeraman", first_light=first_light, lights=[1, 2, 3]
    )


if __name__ == "__main__":
    db.create_all()  # create database
    app.run(debug=True)
