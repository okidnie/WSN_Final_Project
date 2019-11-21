'''
main.py
=======

Author:		Nathan Klassen
Author:		Owen Kidnie

The main file used in this project.
=Makes use of motor.py to find the direction of a Bluetooth signal.
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

def search(rssi, angle):
    direction = -1 #default left
    dir_change = 0

    while(1):
        print("searhing...")
        angle = motor.move(angle, direction)
        rssi_new_list, tx_power_left = getRSSIandTX()
        rssi_new = rssi_new_list[0]

        if rssi > rssi_new:
            print "Changeing Direction"
            direction = direction * -1
            dir_change += 1
            angle = motor.move(angle, direction)
            if dir_change >= 2:
                return angle, rssi

    return angle, rssi

# Main
if __name__=="__main__":
    angle = 90			# Current angle of the motor
    value = 0			# Current RSSI value
    old_rssi = 0		# The max RSSI value in a cycle
    motor.setAngle(90)
    while(1):
        rssi_list, tx_power = getRSSIandTX()
        rssi = rssi_list[0]

        if (abs(rssi-old_rssi) > 5):
            #find node again
            print("Target has moved")
            angle, rssi = search(rssi, angle)
            print("------------")
            print("TARGET FOUND")
            print("------------")


        old_rssi = rssi

    # Debug Receiver value
    print "rssi: {}".format(rssi)

    # Clean motor pwm and GPIO
    motor.motorCleanup()
