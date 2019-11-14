import  RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setup(03, GPIO.OUT)
pwm = GPIO.PWM(03, 50)
pwm.start(0)

def setAngle(angle):
	duty = angle/18 + 2
	#for i in range(20):
	
	#duty = 50
	GPIO.output(03, True)
	pwm.ChangeDutyCycle(duty)
	time.sleep(1)
	GPIO.output(03, False)
	pwm.ChangeDutyCycle(0)
	
#if __name__=="__main__":
#	while True:
#		angle = input("Enter angle: ") 
#		print angle
#		setAngle(angle)
#		time.sleep(2)
#	pwm.stop()
#	GPIO.cleanup()

