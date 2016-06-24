import DS1X31
import time
import requests
import datetime

test = DS1X31.DS1X31(0x48, one_shot = True)

test.init()
test.start()

while(True):
	temp = test.getTemp()
	r = requests.post('http://192.168.168.179:3000/temp', data = {'temp': temp, 'timestamp': datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%S')})
	print temp
        time.sleep(10)
