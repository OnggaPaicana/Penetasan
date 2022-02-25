from app import db
from app.usr import usr
from flask import redirect, render_template, url_for
from app.models import Pengeraman, Tools, delete_record_of_pengeraman
from datetime import datetime, timedelta
import time

# from .utils import *


# Router home
@usr.route("/")
def index() -> render_template:
    return render_template(
        "pages/index.html",
        title="Start",
        timestamp=datetime.utcnow(),
        button="Start",
    )


# Router start
@usr.route("/start")
def start() -> render_template:
    data = Pengeraman.query.get(1)
    tools = Tools.query.all()
    if data is None:
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

    return render_template(
        "pages/pengeraman.html",
        title="Proses Pengeraman",
        timestamp=data.created_at,
        button="Stop",
        tools=tools,
    )


# Router proccess
@usr.route("/proccess")
def proccess() -> render_template:
    data = Pengeraman.query.get(1)

    humy, temp = sensor()  # This still float

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

        if humy <= 55:
            if not fan_off():
                fan_on()

        if temp <= 37:
            if not light_three_off():
                light_two_on()
            elif not light_two_off():
                light_two_on()
            elif not light_one_off():
                light_one_on()

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

    light_one_off()
    light_two_off()
    light_three_off()
    fan_off()
    delete_record_of_pengeraman()

    return render_template(
        "pages/finish.html",
        title="Finished",
    )


# Router second proccess
@usr.route("/second-proccess")
def second_proccess() -> render_template:
    data = Pengeraman.query.get(1)

    while data.day <= 18:
        data.created_at = datetime.utcnow()
        if data.created_at == data.next_day:
            get_next_datetime = datetime.utcnow()
            get_next_datetime += timedelta(days=1)
            data.next_day = get_next_datetime

        time.sleep(28800)
        run_motor()
        time.sleep(7)
        stop_motor()

    stop_motor()

    return render_template(
        "pages/finish.html",
        title="Finished",
    )


# Router stop
@usr.route("/stop")
def stop() -> render_template:
    light_one_off()
    light_two_off()
    light_three_off()
    fan_off()
    delete_record_of_pengeraman()
    return redirect(url_for(".index"))
