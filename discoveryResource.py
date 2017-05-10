import netifaces as ni
import time
import urllib2
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration

def getHomeInfo():
	# get the private IP
	private_ip = ni.ifaddresses('wlan0')[ni.AF_INET][0]['addr']
	print private_ip

	# get the public IP
	response = urllib2.urlopen("http://ipinfo.io/ip")
	public_ip = response.read().rstrip()
	print public_ip

	home_name = "RaspberryPi 1"
	devices = ['RED LED', 'RGB LED', 'Temperature & Humidity Sensor']

	# dict for PubNub
	obj = {"privateIP":private_ip, "publicIP":public_ip, "homeName":home_name, "devices":devices};
	print obj
	return obj

def main():
	pkey = "pub-c-bcc7ac96-ccbe-4577-bd6f-66321585d73a"
	subkey = "sub-c-6d08ffd2-a589-11e6-80e1-0619f8945a4f"

	pnconfig = PNConfiguration()
	pnconfig.subscribe_key = subkey
	pnconfig.publish_key = pkey
	pnconfig.ssl = False
 
	pn = PubNub(pnconfig)
   	#pn = PubNub(publish_key=pkey, subscribe_key=subkey, ssl_on=False)
	home_info = getHomeInfo()
	#pn.publish(channel="smart-home", message=home_info)
	pn.publish().channel('smart-home').message(home_info).async(publish_callback)
		

def publish_callback(result, status):
	print result
	print status
if __name__ == "__main__":
	for i in xrange(6):
		main()
		time.sleep(10)
  
