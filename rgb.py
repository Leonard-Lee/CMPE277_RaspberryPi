#!/usr/bin/python

import time
import RPi.GPIO as GPIO

## Make your pin assignments
red_gpio   = 6
green_gpio = 5
blue_gpio  = 22

## Setup GPIO Board and Pins
GPIO.setmode(GPIO.BCM)    # BCM for GPIO numbering  
GPIO.setup(red_gpio,   GPIO.OUT)
GPIO.setup(green_gpio, GPIO.OUT)
GPIO.setup(blue_gpio,  GPIO.OUT)

## Init the GPIO PWMs
Freq  = 100 #Hz

RED   = GPIO.PWM(red_gpio, Freq)
RED.start(0)

GREEN = GPIO.PWM(green_gpio, Freq)
GREEN.start(0)

BLUE  = GPIO.PWM(blue_gpio, Freq)
BLUE.start(0)

def updateHue(R, G, B):
	rVal = (R/255.0)*100	# Will have to change these values depending on
	gVal = (G/255.0)*100	#  whether your LED has a common cathode or common
	bVal = (B/255.0)*100	#  anode. This code is for common anode.
	print "rgb(%.2f, %.2f, %.2f)" % (rVal, gVal, bVal)
	RED.ChangeDutyCycle(rVal)
	GREEN.ChangeDutyCycle(gVal)
	BLUE.ChangeDutyCycle(bVal)

def rgb():
	updateHue(255,0,0)
	time.sleep(2)
	
	updateHue(0,255,0)
	time.sleep(2)
	
	updateHue(0,0,255)
	time.sleep(2)

def main():
	rgb()
	updateHue(0,0,0); # Light off
	
main()
