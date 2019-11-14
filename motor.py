'''
This file controls a motor through GPIO pinout 3 of a raspberry pi 3.

Authors:
Nathan Klassens
Owen Kidnie
'''

import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm = GPIO.PWM(03, 50)
pwm.start(0)

def setAngle(angle):
	duty = angle/18 + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)

def move(angle, direction):
	if direction == 0:
		print "Try turning left"
		angle = angle + 18
		setAngle(angle)
	else:
		print "Try turning right"
		angle = angle - 18
		setAngle(angle)

	return angle

def motorCleanup():
	pwm.stop()
	GPIO.cleanup()


