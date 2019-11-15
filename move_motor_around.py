'''
Used to test out control over the motor

Authors:
Nathan Klassens
Owen Kidnie 
'''

import motor
import time 

if __name__=="__main__":
	while True:
		angle = input("Enter angle: ") 
		print angle
		motor.setAngle(angle)
		time.sleep(2)
		
	motor.motorCleanup()

