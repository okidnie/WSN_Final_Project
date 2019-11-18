'''
main.py
=======

Author:		Nathan Klassen
Author:		Owen Kidnie

The main file used in this project.
Makes use of motor.py to find the direction of a Bluetooth signal.
Beacon scanner code taken from https://github.com/switchdoclabs/iBeacon-Scanner-.git.
'''

from __future__ import division
import os
import numpy as np
import pylab
import re
import subprocess
import math
import operator
import blescan
import motor
import sys
import bluetooth._bluetooth as bluez
import time

beacons = ["a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"] # List of beacon UUIDs
iterations = 25 # Number of times the pi scans for the beacons

num_beacons = len(beacons)

def getRSSIandTX():
	'''
	Obtains the RSSI and TX values of the packet
	:return: rssi, and tx_power
	'''

	# Value containers
	rssi = [[]]
	tx_power = [[]]
	
	# Open BLE socket
	try:
		sock = bluez.hci_open_dev(0)
		print "Start BLE communication"
	except:
		print "error accessing bluetooth device..."
		sys.exit(1)


	blescan.hci_le_set_scan_parameters(sock)
	blescan.hci_enable_le_scan(sock)

	# Loop to scan the beacons
	for x in range(iterations):
		
		returnedList = blescan.parse_events(sock, 10)
		for beacon in returnedList:
			details = beacon.split(',')

			# If scanned beacon is among the listed, store its RSSI and TX Power
			if details[1] in beacons:
				rssi[beacons.index(details[1])].append(float(details[5]))
				tx_power[beacons.index(details[1])].append(float(details[4]))
	
	# Makeshift data filter. Try to play around with this part of the code to get the best quality of RSSI and Tx_Power values
	for x in range(num_beacons):
		#Mean Filter
		rssi[x] = sum(rssi[x])/float(len(rssi[x]))
		tx_power[x] = sum(tx_power[x])/float(len(tx_power[x]))
	
	
	print ("node ", rssi[0]," : ",  tx_power[0])
	return rssi, tx_power

# Calculates the distance between two points of interest using RSSI and TX Power
def pathloss(rssi, tx_power):
	'''
	Calculates the distance between two points of interest using RSSI and TX Power

	:param rssi: 		The RSSI of the packet
	:param tx_power: 	The TX power of the packet
	:return:			The distance from the packet
	'''

	n = 2.0
	distance = 10.0**((tx_power - rssi) / (10.0 * n))

	return distance
	
# Calculate location of poit of interest based on its distance from 3 defined points
def trilateration(d1, d2, d3, p, q, r):
	x = (d1**2 - d2**2 + p**2) / (2.0 * p)
	y = ((d1**2 - d2**2 + q**2 + r**2) / (2.0 * r)) - ((q / r) * x)
	
	receiver = []
	receiver.append(x)
	receiver.append(y)
	return receiver

# Main
if __name__=="__main__":
	angle = 0			# Current angle of the motor
	value = 0			# Current RSSI value
	direction = 0 		# 0 if turn left, 1 is turn right
	max_val = 0			# The max RSSI value in a cycle
	searching = False	# wether the system needs to be searching for signal direction or not
	range_factor = 2	# error value
	for i in range(10):
		print "----------------------------"
		rssi, tx_power = getRSSIandTX()
		val_range = range(round(rssi[0]) - range_factor, round(rssi[0]) + range_factor, 1)
		old_val = value
		max_val = value

		# Transmitter has changed position so set range back to default to attempt best accuracy
		if value not in val_range:
			range_factor = 2
			searching = True

		while searching == True:
			angle = motor.move(angle, direction)

			rssi, tx_power = getRSSIandTX()
			value = round(rssi[0])

			# Value is smaller then previous so change direction
			if value < old_val:
				direction = 1 if direction == 0 else 0  # Change direction

			# Value is now getting smaller again so we have passed closest position
			if value < max_val:
				angle = motor.move(angle, direction)	# Move motor back a position
				rssi, tx_power = getRSSIandTX()
				searching = False
				print ("This is as close as I can get")
				d1 = pathloss(rssi[0], tx_power[0])
				print ("The distance to transmitter is: {}".format(d1))

			max_val = max([value, max_val])
			old_val = value

		value = rssi
		print "rssi: {}".format(rssi)
		print "----------------------------"

	rssi, tx_power = getRSSIandTX()
	d1 = pathloss(rssi[0])

	# Debug Receiver value
	print "rssi: {}".format(rssi)

	# Clean motor pwm and GPIO
	motor.motorCleanup()



