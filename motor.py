'''
motor.py
========

Author:		Nathan Klassen
Author:		Owen Kidnie

Controls a servo motor through GPIO pinouts on a raspberry pi 3.
'''

import RPi.GPIO as GPIO
import time

servoPin = 03
LEDPin = 04
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPin, GPIO.OUT)
GPIO.setup(LEDPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50)
pwm.start(0)

def LEDToggle(mode):
    '''
    Toggles an led using the GPIO pin set at LEDPin

    :param mode:    True turns LED on and False turns LED off
    '''

    GPIO.output(LEDPin, mode)

def setAngle(angle):
    '''
    Sets the angle of the servo motor

    :param angle:   the desired angle to set the servo motor to
    '''

    duty = angle/18 + 2
    GPIO.output(servoPin, True)
    pwm.ChangeDutyCycle(duty)
    time.sleep(1)
    GPIO.output(servoPin, False)
    pwm.ChangeDutyCycle(0)

def move(angle, direction):
    '''
    Moves the servo motor left or right by 18 degrees

    :param angle:       The current angle of the servo motor
    :param direction:   The desired direction (left or right)
    :return:            The new angle of the servo motor
    '''

    if direction == 1:
        print "Turning right"
        angle = angle + 18
    elif direction == -1:
        print "Turning left"
        angle = angle - 18

    if angle > 180:
        angle = 180
    elif angle < 0:
        angle = 0

    setAngle(angle)
    time.sleep(0.5)
    return angle

def motorCleanup():
    '''
    cleans up GPIO pin and stops servo motor
    '''

    pwm.stop()
    GPIO.cleanup()

def motorFullSpin():
    '''
    moves the servo motor back and fourth (180 degrees).
    Used for testing purposes.
    '''

    print("Starting to spin\n")
    try:
        while True:
            pwm.ChangeDutyCycle(0)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(2.5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(10)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(12.5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(10)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(7.5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(2.5)
            time.sleep(0.5)
            pwm.ChangeDutyCycle(0)
            time.sleep(0.5)
    except KeyboardInterrupt:
        motorCleanup()

def controlMotorAngle():
    '''
    Allows user to input desired angle for servo motor to point to.
    Used for testing purposes.
    '''

    try:
        while True:
            angle = input("Enter angle: ")
            print angle
            setAngle(angle)
            time.sleep(0.5)
    except KeyboardInterrupt:
        motorCleanup()
