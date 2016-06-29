import DS1X31
import time
import requests
from datetime import datetime 
import pytz

test = DS1X31.DS1X31(0x48, one_shot = True)

test.init()
test.start()

print 'Temperature data being collected and sent to http://192.168.168.5:3000...'
while(True):
	temp = test.getTemp()
	unaware = datetime.now()
	tz = pytz.timezone('US/Eastern')
	now = tz.localize(unaware)
	r = requests.post('http://192.168.168.5:3000/temp', data = {'temp': temp, 'timestamp': now.strftime('%Y-%m-%dT%H:%M:%S%z')})
        time.sleep(10)
