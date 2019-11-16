'''
Used to test out control over the motor

Authors:
Nathan Klassens
Owen Kidnie 
'''

import motor
import time 

if __name__=="__main__":
	option = input("Would you like to control the angle? Yes(1) or No(0)? ")
	
	if option == 1:	
		motor.controlMotorAngle()
	else:
		motor.motorFullSpin()

