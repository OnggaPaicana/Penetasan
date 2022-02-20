from turtle import title
from flask import Flask, render_template, url_for
from flask_moment import Moment
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
import os

# Konfigurasi untuk folder aplikasi
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
moment= Moment(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///datetime.db'
db = SQLAlchemy(app)

# membuat tabel
class pengeraman(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tanggal =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    bulan =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    tahun =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    jam =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    menit =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    detik =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    waktu_mulai =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)
    total_hari =db.Column(db.DateTime, unique=True, nullable=False,  default=datetime.utcnow)

def __repr__(self):
		return "id: {}, waktu mulai: {}, tanggal: {}, bulan: {},tahun: {}, jam: {}, menit: {}, detik: {}, Total Hari: {}".format(self.waktu_mulai, self.tanggal, self.bulan, self.tahun, self.jam, self.menit, self.detik, self.total_hari)
        
db.create_all()
# Sensor untuk DHT11
    
@app.route("/")
def index():
    return render_template('index.html',waktu=datetime.utcnow(),title='Mulai Pengeraman')



@app.route("/start")
def start():
    return render_template('pengeraman.html', pengeraman =pengeraman.query.all(), title='Proses Pengeraman')


if __name__ == '__main__':
    app.run(debug=True)