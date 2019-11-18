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
servo2Pin = 04
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servo1Pin, GPIO.OUT)
GPIO.setup(servo2Pin, GPIO.OUT)
pwm1 = GPIO.PWM(servo1Pin, 50)
pwm2 = GPIO.PWM(servo2Pin, 50)
pwm1.start(0)
pwm2.start(12.5)


def setAngle(angle, servoPin=servo1Pin, pwm=pwm1):
	'''
	Sets the angle of the servo motor
	:param angle: the desired angle to set the servo motor to
	'''

	duty = angle/18 + 2
	GPIO.output(servoPin, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(servoPin, False)
	pwm.ChangeDutyCycle(0)

def move(angle, direction, servoNum):
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
		if servoNum == 1:
			servoNum = 2
			angle = 18
			setAngle(180, servo1Pin, pwm1)
			setAngle(angle, servo2Pin, pwm2)
		else:
			servoNum = 1
			angle = 18
			setAngle(angle, servo1Pin, pwm1)
			setAngle(0, servo2Pin, pwm2)
	elif angle < 0:
		if servoNum == 1:
			servoNum = 2
			angle = 162
			setAngle(angle, servo2Pin, pwm2)
			setAngle(180, servo1Pin, pwm1)
		else:
			servoNum = 1
			angle = 162
			setAngle(0, servo2Pin, pwm2)
			setAngle(angle, servo1Pin, pwm1)
	else:
		if servoNum == 1:
			setAngle(angle, servo1Pin, pwm1)
		else:
			setAngle(angle, servo2Pin, pwm2)

	return angle, servoNum

def motorCleanup():
	'''
	cleans up GPIO pin and stops servo motor
	'''
	pwm1.stop()
	GPIO.cleanup()
	
def motorFullSpin():
	'''
	moves the servo motor back and fourth (180 degrees).  Used for testing purposes.
	'''

	print("Starting to spin\n")
	try:
		while True:
			pwm1.ChangeDutyCycle(0)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(2.5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(7.5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(10)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(12.5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(10)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(7.5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(2.5)
			time.sleep(0.5)
			pwm1.ChangeDutyCycle(0)
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


