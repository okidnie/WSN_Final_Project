'''
Used to test out control over the motor

Authors:
Nathan Klassens
Owen Kidnie 
'''

import motor

if __name__=="__main__":
	while True:
		angle = input("Enter angle: ") 
		print angle
		setAngle(angle)
		time.sleep(2)

