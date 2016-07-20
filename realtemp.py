import time
import requests
from datetime import datetime 
import pytz
from pyowm import OWM
import json

print 'Real Temperature data being collected and sent to http://192.168.168.5:3000...'
while(True):
	temp = 0
	apiKey = '60f317d055265f90f81f6157503f89a6'
	owm = OWM(apiKey)
	
	try:
		obs = owm.weather_at_id(5202765)#Murrysville
		weather = obs.get_weather()
		tempobj = weather.get_temperature('fahrenheit')
		temp = tempobj['temp']		
		unaware = datetime.now()
		tz = pytz.timezone('US/Eastern')
		now = tz.localize(unaware)
		formatString = now.strftime('%Y-%m-%dT%H:%M:%S%z')
		r = requests.post('http://192.168.168.5:3000/realtemp', data = {'temp': temp, 'timestamp': formatString})
		printout = "temp: %s, timestamp: %s" % (temp, formatString)
		print printout
	except:
		#error
		print 'unable to retrieve temperature data'
		

        time.sleep(600)
