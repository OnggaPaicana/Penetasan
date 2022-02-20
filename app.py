import click
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

    def __repr__(self):
        return "<Name {}>".format(self.name)


class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    active = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
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
    return render_template("pages/index.html", title="Start", timestamp=datetime.utcnow(), button="Start")


@app.route("/start")
def start():
    first_light = True
    first_data = Pengeraman.query.get(1)
    tools = Tools.query.all()
    timestamp = first_data.created_at
    return render_template(
        "pages/pengeraman.html",
        title="Proses Pengeraman",
        first_light=first_light,
        lights=[1, 2, 3],
        timestamp=timestamp,
        button="Stop",
        tools=tools,
    )


# make command of flask
@app.cli.command()
def deploy():
    """Insert Tools to Database"""
    first_tool = Tools(name="Lampu 1")
    second_tool = Tools(name="Lampu 2")
    third_tool = Tools(name="Lampu 3")
    fourth_tool = Tools(name="Motor")
    fifth_tool = Tools(name="Kipas")

    db.session.add_all([first_tool, second_tool, third_tool, fourth_tool, fifth_tool])
    db.session.commit()
    print("All tools created.")


@app.cli.command()
def create_table():
    """Create tables"""
    db.create_all()
    print("Table created.")


if __name__ == "__main__":
    app.run(debug=True)
