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

beacons = ["a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1a1"]  # List of beacon UUIDs

iterations = 20  # Number of times the pi scans for the beacons

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

    # Makeshift data filter. Try to play around with this
    # part of the code to get the best quality of RSSI and Tx_Power values.
    # The first 10 RSSI readings are filtered out to try and mitigate outlying values
    for x in range(num_beacons):
        # Mean Filter
        try:
            rssi[x] = sum(rssi[x][10:])/float(len(rssi[x][10:]))
            tx_power[x] = sum(tx_power[x])/float(len(tx_power[x]))
        except:
            print "lost connection"
            return [0],[0]
                

    return rssi, tx_power

def pathloss(rssi, tx_power):
    '''
    Calculates the distance between two points of interest using RSSI and TX Power

    :param rssi: 		The RSSI of the packet
    :param tx_power:    The TX power of the packet
    :return:			The distance from the packet
    '''

    n = 2.0
    distance = 10.0**((tx_power - rssi) / (10.0 * n))

    return distance

def search(rssi, angle):
    '''
    Searches for the position of stringest RSSI

    :param rssi:    The current RSSI value
    :param angle:   The current angle of the servo motor
    :return:        The stringest RSSI value found, and the angle of that reading
    '''

    direction = -1 #default is left
    dir_change = 0
    times_moved = 0
    rssi_dict = {}

    rssi_dict[angle] = rssi

    while(1):
        print("searhing...")
        angle = motor.move(angle, direction)
        times_moved += 1
        rssi_new_list, tx_power_left = getRSSIandTX()
        rssi_new = rssi_new_list[0]
        
        print "rssi: ", rssi
        rssi_dict[angle] = rssi_new
        if rssi > rssi_new and rssi_new != 0:
            print "Changeing Direction"
            direction = direction * -1
            dir_change += 1
            angle = motor.move(angle, direction)
            if (dir_change >= 2 and times_moved < 2) or (dir_change < 2 and times_moved > 2):
                print rssi_dict
                print angle
                return angle, rssi_new
            times_moved = 0  
        elif angle == 0 or angle == 180:
            print "Changeing Direction"
            direction = direction * -1
            dir_change += 1
            angle = motor.move(angle, direction)
            times_moved = 0
        elif rssi_new != 0:
            rssi = rssi_new
            rssi_dict[angle] = rssi_new

    return angle, rssi

# Main
if __name__=="__main__":
    angle = 90			# Current angle of the motor
    value = 0			# Current RSSI value
    old_rssi = 0		# previous RSSI value

    motor.setAngle(90)
    motor.LEDToggle(False)

    while(1):
        rssi_list, tx_power = getRSSIandTX()
        rssi = rssi_list[0]
        print rssi

        if ((abs(rssi-old_rssi) > 5) and (rssi != 0)):
            #find node again
            print("Target has moved")
            motor.LEDToggle(False)
            angle = 90
            motor.setAngle(90)
            rssi_list, tx_power = getRSSIandTX()
            rssi = rssi_list[0]
            angle, rssi = search(rssi, angle)
            print("------------")
            print("TARGET FOUND")
            print("------------")
            motor.LEDToggle(True)

        if rssi != 0:
            old_rssi = rssi

    # Debug Receiver value
    print "rssi: {}".format(rssi)

    # Clean motor pwm and GPIO
    motor.motorCleanup()
