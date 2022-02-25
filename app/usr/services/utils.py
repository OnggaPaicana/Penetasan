from typing import Any
from Adafruit_DHT import read_retry
import RPi.GPIO as GPIO


def sensor() -> Any:
    humidity, temperature = read_retry(11, 4)
    return humidity, temperature


GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)


# To run motor
def run_motor() -> bool:
    return GPIO.output(7, GPIO.LOW)


# To stop motor()
def stop_motor() -> bool:
    return GPIO.output(7, GPIO.HIGH)


# To light_one_on
def light_one_on() -> bool:
    return GPIO.output(23, GPIO.LOW)


# To light_one_off
def light_one_off() -> bool:
    return GPIO.output(23, GPIO.HIGH)


# To light_two_on
def light_two_on() -> bool:
    return GPIO.output(23, GPIO.LOW)


# To light_two_off
def light_two_off() -> bool:
    return GPIO.output(23, GPIO.HIGH)


# To light_three_on
def light_three_on() -> bool:
    return GPIO.output(24, GPIO.LOW)


# To light_three_off
def light_three_off() -> bool:
    return GPIO.output(24, GPIO.HIGH)


# To fan on
def fan_on() -> bool:
    return GPIO.output(8, GPIO.LOW)


# To fan off
def fan_off() -> bool:
    GPIO.output(8, GPIO.HIGH)
    return False
