#Beacon scanner code taken from https://github.com/switchdoclabs/iBeacon-Scanner-.git 

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
from gpiozero import LED
import  RPi.GPIO as GPIO

nodes = [0,7,9,7,0,0,9,0] # Change this based on coordinates of you beacons - Format:[Ax, Ay, Bx, By ... ]
beacons = ["a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"] # List of beacon UUIDs
iterations = 25 # Number of times the pi scans for the beacons

num_beacons = len(beacons)

# Obtain the RSSI and TX values of each packet
def getRSSIandTX():
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
			#print beacon
			details = beacon.split(',')
			#print beacon
			
			# If scanned beacon is among the listed, store its RSSI and TX Power
			if details[1] in beacons:
				rssi[beacons.index(details[1])].append(float(details[5]))
				tx_power[beacons.index(details[1])].append(float(details[4]))
	
	# Makeshift data filter. Try to play around with this part of the code to get the best quality of RSSI and Tx_Power values
	for x in range(num_beacons):
		#Mode Filter
		#rssi[x] = max(set(rssi[x]), key=rssi[x].count)
		#tx_power[x] = max(set(tx_power[x]), key=tx_power[x].count)
		
		#Mean Filter
		rssi[x] = sum(rssi[x])/float(len(rssi[x]))
		tx_power[x] = sum(tx_power[x])/float(len(tx_power[x]))
	
	
	print ("node ", rssi[0]," : ",  tx_power[0])
	#print ("2nd element ", rssi[1]," : ",  tx_power[1]) 
	#print ("3rd element ", rssi[2]," : ",  tx_power[2]) 
	#print ("4th element ", rssi[3]," : ",  tx_power[3])  
	
	#sorted(rssi, reverse=True)
	#sorted(tx_power, reverse=True)
	#rssi.sort(reverse=True)
	#tx_power.sort(reverse=True)
	#print ("1st element sorted ", rssi[0]," : ",  tx_power[0])
	#print ("2nd element sorted", rssi[1]," : ",  tx_power[1]) 
	#print ("3rd element sorted", rssi[2]," : ",  tx_power[2]) 
	#print ("4th element sorted", rssi[3]," : ",  tx_power[3]) 
	
		
	return rssi, tx_power

# Calculates the distance between two points of interest using RSSI and TX Power
def pathloss(rssi, tx_power):
	n = 2.0
	distance = 10.0**((tx_power - rssi) / (10.0 * n))
	
	print distance
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
	angle = 0
	value = 0
	val_small = 0
	direction = 0 		# 0 if left, 1 is right
	lowest_val = 0
	for i in range(10):
		print "----------------------------"
		rssi, tx_power = getRSSIandTX()
		round_rssi = round(rssi[0])
		val_range = [round_rssi-2, round_rssi-1, round_rssi, round_rssi+1, round_rssi+2]
		while value not in val_range:
			old_val = value
			if direction == 0:
				print "Try Left"
				angle = angle + 18
				motor.setAngle(angle)
			else:
				print "Try Right"
				angle = angle - 18
				motor.setAngle(angle)
			rssi, tx_power = getRSSIandTX()
			value = round(rssi[0])
			if value < old_val:
				direction = 1 if direction == 0 else 0
			val_list = [value, old_val, lowest_val]
			lowest_val = max(val_list)
			
		value = round_rssi
		print "rssi: {}".format(rssi)
		print "----------------------------"
	
	rssi, tx_power = getRSSIandTX()
	d1 = pathloss(rssi[0], tx_power[0])
	#d2 = pathloss(rssi[1], tx_power[1])
	#d3 = pathloss(rssi[2], tx_power[2])
	p = 14 # X-axis Bound
	q = 0 # Z-axis Bound
	r = 16 # Y-axis Bound
	#receiver = trilateration(d1, d2, d3, p, q, r)
	#print receiver # Debug Receiver value
	print "rssi: {}".format(rssi)
	# Plot data
	#pylab.plot(nodes[0], nodes[1], 'bs')
	#pylab.plot(nodes[2], nodes[3], 'rs')
	#pylab.plot(nodes[4], nodes[5], 'gs')
	#pylab.plot(nodes[6], nodes[7], 'ys')
	#pylab.plot(receiver[0], receiver[1], 'k^')

	#pylab.xlabel('X')
	#pylab.ylabel('Y')
	#pylab.legend(('Beacon A1', 'Beacon B2', 'Beacon C3', 'Beacon D4', 'Receiver'))
	#pylab.grid()
	#pylab.show()


