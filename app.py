from flask import Flask, redirect, render_template, request, url_for
from flask_moment import Moment
from datetime import datetime, timedelta
#from Adafruit_DHT import read_retry
#import RPi.GPIO as GPIO
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap5
import os, time

# Get path
basedir = os.path.abspath(os.path.dirname(__file__))

#GPIO.setmode(GPIO.BCM)
#GPIO.setwarnings(False)
#GPIO.setup(23, GPIO.OUT) # Lampu 1 dan2
#GPIO.setup(24, GPIO.OUT) # Lampu 3
#GPIO.setup(7, GPIO.OUT) # Motor AC
#GPIO.output(8, GPIO.OUT) #Fan

# Identifikasi GPIO
#lampu1_2_nyala = GPIO.output(23, GPIO.LOW)
# #lampu1_2_mati = GPIO.output(23, GPIO.HIGH)
#lampu_3_nyala = GPIO.output(24, GPIO.LOW)
#lampu_3_mati = GPIO.output(24, GPIO.HIGH)
#stop_motor = GPIO.output(7, GPIO.HIGH)
#run_motor = GPIO.output(7, GPIO.LOW)
#fan_off = GPIO.output(8, GPIO.HIGH)
#fan_on = GPIO.output(8, GPIO.LOW)

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
    total_days = db.Column(db.Integer, default=0)
    day = db.Column(db.Integer, default=1)
    next_day = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return "<Name {}>".format(self.name)


# Delete all record in Pengeraman
def delete_record_of_pengeraman() -> None:
    records = Pengeraman.query.all()
    for record in records:
        db.session.delete(record)
        db.session.commit()

# To run motor
def run_motor() -> bool:
    #GPIO.output(7, GPIO.LOW)
    return True


# To stop motor()
def stop_motor() -> bool:
    #GPIO.output(7, GPIO.HIGH)
    return False


# To light_one_on
def light_one_on() -> bool:
    #GPIO.output(23, GPIO.LOW)
    return True

# To light_one_off
def light_one_off() -> bool:
    #lampu_1_mati = GPIO.output(23, GPIO.HIGH)
    return False


# To light_two_on
def light_two_on() -> bool:
    #GPIO.output(23, GPIO.LOW)
    return True


# To light_two_off
def light_two_off() -> bool:
    #GPIO.output(23, GPIO.HIGH)
    return False


# To light_three_on
def light_three_on() -> bool:
    #GPIO.output(24, GPIO.LOW)
    return True


# To light_three_off
def light_three_off() -> bool:
     #GPIO.output(24, GPIO.HIGH)
    return False


# To fan on
def fan_on() -> bool:
    #GPIO.output(8, GPIO.LOW)
    return True


# To fan off
def fan_off() -> bool:
    #GPIO.output(8, GPIO.HIGH)
    return False


# Create table tools
class Tools(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    active = db.Column(db.Boolean, default=False)

    def __repr__(self) -> str:
        return "<Name {}>".format(self.name)


# Router home
@app.route("/", methods=["GET", "POST"])
def index() -> render_template:
    if request.method == "POST":
        # assignment date and time
        get_datetime = datetime.utcnow()
        get_next_datetime = datetime.utcnow()
        get_next_datetime += timedelta(days=1)

        # assignment data
        data = Pengeraman(day=1, total_days=1)
        data.created_at = get_datetime
        data.next_day = get_next_datetime

        # add data
        db.session.add(data)

        # push data to database
        db.session.commit()
        return redirect(url_for("start"))
    return render_template("pages/index.html", title="Start", timestamp=datetime.utcnow(), button="Start")


# Router start
@app.route("/start")
def start() -> render_template:
    data = Pengeraman.query.get(1)
    tools = Tools.query.all()
    timestamp = data.created_at

    return render_template(
        "pages/pengeraman.html",
        title="Proses Pengeraman",
        timestamp=timestamp,
        button="Stop",
        tools=tools,
    )

#def sensor():
	#humidity, temperature = read_retry(11, 4)
	#return humidity, temperature

@app.route("/background")
def background() -> render_template:
    data = Pengeraman.query.get(1)
    tools = Tools.query.all()
    timestamp = data.created_at

    # Ubah temp with data real time temperature
    #data = sensor()
    #temp = request.form["temp"]
	#humy = request.form["humy"]
    temp = 0
    humy = 0

    # putar rak 3 kali selang waktu 8 jam
    # time.sleep(28800)
    # run_motor()
    # time.sleep(7)
    # stop_motor()

    while data.day <= 18:
        data.created_at = datetime.utcnow()
        if data.created_at == data.next_day:
            get_next_datetime = datetime.utcnow()
            get_next_datetime += timedelta(days=1)
            data.next_day = get_next_datetime
            db.session.add(data)
            db.session.commit()

        # Logic for temp
        if temp >= 38:
            if light_three_on():
                light_two_off()
            elif light_two_on():
                light_two_off()
            elif light_one_on():
                light_one_off()

        if temp <= 37:
            if not light_three_off():
                light_two_on()
            elif not light_two_off():
                light_two_on()
            elif not light_one_off():
                light_one_on()

        # Logic for humy
        if humy <= 55:
            if not fan_off():
                fan_on()
        if humy >= 60:
            if fan_on():
                fan_off()

    while data.day <= 21:
        # Logic for temp
        if temp >= 37:
            if light_three_on():
                light_two_off()
            elif light_two_on():
                light_two_off()
            elif light_one_on():
                light_one_off()
        else:
            if not light_three_off():
                light_two_on()
            elif not light_two_off():
                light_two_on()
            elif not light_one_off():
                light_one_on()

        # Logic for humy
        if humy <= 70:
            if not fan_off():
                fan_on()
        else:
            if fan_on():
                fan_off()

    return render_template(
        "pages/pengeraman.html",
        title="Proses Pengeraman",
        timestamp=timestamp,
        button="Stop",
        tools=tools,
    )


# make command insert of flask
@app.cli.command()
def insert() -> None:
    """Insert Tools to Database"""
    first_tool = Tools(name="Lampu 1")
    second_tool = Tools(name="Lampu 2")
    third_tool = Tools(name="Lampu 3")
    fourth_tool = Tools(name="Motor")
    fifth_tool = Tools(name="Kipas")

    db.session.add_all([first_tool, second_tool, third_tool, fourth_tool, fifth_tool])
    db.session.commit()
    print("All tools created.")


# make command create table of flask
@app.cli.command()
def create_table() -> None:
    """Create tables"""
    db.create_all()
    print("Table created.")


if __name__ == "__main__":
    app.run(debug=True)