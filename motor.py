'''
motor.py
========

Author:		Nathan Klassen
Author:		Owen Kidnie

Controls a servo motor through GPIO pinouts on a raspberry pi 3.
'''

import RPi.GPIO as GPIO
import time

servo1Pin = 03
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1Pin, GPIO.OUT)
pwm = GPIO.PWM(servo1Pin, 50)
pwm.start(0)


def setAngle(angle):
	'''
	Sets the angle of the servo motor
	:param angle: the desired angle to set the servo motor to
	'''

	duty = angle/18 + 2
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)

def move(angle, direction):
	'''
	Moves the servo motor left or right by 18 degrees
	:param angle: 		The current angle of the servo motor
	:param direction: 	The desired direction (left or right)
	:return: 			The new angle of the servo motor
	'''

	if direction == 0:
		print "Try turning left"
		angle = angle + 18
	else:
		print "Try turning right"
		angle = angle - 18

	if angle > 180:
		angle = 180
	elif angle < 0:
		angle = 0

	setAngle(angle)
	return angle

def motorCleanup():
	'''
	cleans up GPIO pin and stops servo motor
	'''
	pwm.stop()
	GPIO.cleanup()
	
def motorFullSpin():
	'''
	moves the servo motor back and fourth (180 degrees).  Used for testing purposes.
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
	Allows user to input desired angle for servo motor to point to.  Used for testing purposes
	'''
	try:
		while True:
			angle = input("Enter angle: ") 
			print angle
			setAngle(angle)
			time.sleep(0.5)
	except KeyboardInterrupt:
		motorCleanup()


