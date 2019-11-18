'''
move_motor_around.py
====================

Author:		Nathan Klassen
Author:		Owen Kidnie

Used for testing the motor through user input in the terminal.
To run through terminal: sudo python move_motor_around.py
'''

import motor
import time 

if __name__=="__main__":
	option = input("Would you like to control the angle? Yes(1) or No(0)? ")
	
	if option == 1:	
		motor.controlMotorAngle()
	else:
		motor.motorFullSpin()

