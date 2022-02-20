from turtle import title
from flask import Flask, render_template, url_for
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

# Get path
basedir = os.path.abspath(os.path.dirname(__file__))


# Initialize app
app = Flask(__name__)
moment= Moment(app)
db = SQLAlchemy(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# Create Tabel Pengeraman
class Pengeraman(db.Model):
    id = db.Column("pengeraman_id", db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    created_at = db.Column(db.Datetime, nullable=False)
    updated_at = db.Column(db.Datetime, nullable=False)

    def __init__(self):
        pass
    
    def __repr__(self):
        return "<Name {}>".format(self.name)

# Router
@app.route("/")
def index():
    return render_template('index.html', waktu=datetime.utcnow(), title='Mulai Pengeraman')



@app.route("/start")
def start():
    return render_template('pengeraman.html', pengeraman=pengeraman.query.all(), title='Proses Pengeraman')


if __name__ == '__main__':
    app.run(debug=True)