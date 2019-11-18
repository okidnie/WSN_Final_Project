'''
This file controls a motor through GPIO pinout 3 of a raspberry pi 3.

Authors:
Nathan Klassen
Owen Kidnie
'''

import RPi.GPIO as GPIO
import time

servoPin = 03
GPIO.setmode(GPIO.BOARD)
GPIO.setup(servoPin, GPIO.OUT)
pwm = GPIO.PWM(servoPin, 50)
pwm.start(2.5)

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
	
def motorFullSpin():
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
	try:
		while True:
			angle = input("Enter angle: ") 
			print angle
			motor.setAngle(angle)
			time.sleep(0.5)
	except KeyboardInterrupt:
		motorCleanup()


