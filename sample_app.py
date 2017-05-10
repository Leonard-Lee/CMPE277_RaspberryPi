from flask import Flask, request, jsonify
import RPi.GPIO as GPIO
import time
import sys
import Adafruit_DHT

first_app = Flask(__name__)
first_app.config['DEBUG'] = True

@first_app.route("/")
def welcome():
        return "<html><body><h1 style='color:blue'>Welcome world123!!!</h1></body></html>"

@first_app.route("/red", methods=["GET"])
def red():
	return jsonify({'result': 'Off'}) 

	#GPIO.cleanup()

@first_app.route("/rgb", methods=["GET"])
def rgb():
	## Make your pin assignments
	red_gpio   = 6
	green_gpio = 5
	blue_gpio  = 22

	## Setup GPIO Board and Pins
	GPIO.setmode(GPIO.BCM)    # BCM for GPIO numbering
	GPIO.setup(red_gpio,   GPIO.OUT)
	GPIO.setup(green_gpio, GPIO.OUT)
	GPIO.setup(blue_gpio,  GPIO.OUT)

	## HTTP GET Parameters
	R = int(request.args.get("r"))
	G = int(request.args.get("g"))
	B = int(request.args.get("b"))
	print "HTTP GET rgb(%d, %d, %d)" % (R, G, B) 

	## Init the GPIO PWMs
	Freq  = 100 #Hz

	RED   = GPIO.PWM(red_gpio, Freq)
	RED.start(0)

	GREEN = GPIO.PWM(green_gpio, Freq)
	GREEN.start(0)

	BLUE  = GPIO.PWM(blue_gpio, Freq)
	BLUE.start(0)

	def updateHue(R, G, B):
		rVal = (R/255.0)*100    # Will have to change these values depending on
		gVal = (G/255.0)*100    #  whether your LED has a common cathode or common
		bVal = (B/255.0)*100    #  anode. This code is for common anode.
		#print "rgb(%.2f, %.2f, %.2f)" % (rVal, gVal, bVal)
		RED.ChangeDutyCycle(rVal)
		GREEN.ChangeDutyCycle(gVal)
		BLUE.ChangeDutyCycle(bVal)

	updateHue(R,G,B)
	#updateHue(255, 0, 0)
	#time.sleep(4)
	#GPIO.cleanup()
	return jsonify({'result': 'success'}) 

@first_app.route("/temphumid", methods=["GET"])
def temphumid():
	sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
	sensor = sensor_args['11']
    	pin = 17 			##BCM PIN PORT

	# Try to grab a sensor reading.  Use the read_retry method which will retry up
	# to 15 times to get a sensor reading (waiting 2 seconds between each retry).
	humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

	# Un-comment the line below to convert the temperature to Fahrenheit.
	temperature = temperature * 9/5.0 + 32

	# Note that sometimes you won't get a reading and
	# the results will be null (because Linux can't
	# guarantee the timing of calls to read the sensor).
	# If this happens try again!
	if humidity is not None and temperature is not None:
		'{:0.2f}'.format(3.141592653589793)
		strTemp = '{:0.2f}*F'.format(temperature)
		strHumidity = '{:0.2f}%'.format(humidity)
			
		return jsonify({'result': 'success', 'temp': strTemp, 'humidity': strHumidity}) 
	else:
		return jsonify({'result': 'success', 'temp': '-9999.99', 'humidity': '-9999.99'}) 
	    
if __name__ == "__main__":
	first_app.run(host='0.0.0.0')
