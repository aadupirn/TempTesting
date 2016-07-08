import time
import requests
from datetime import datetime 
import pytz
import sys
import uuid

if len(sys.argv) <= 1:
    print "Not enough arguments! exiting..."
    exit()
else:
    if sys.argv[1].lower() == 'edison':
        import DS1X31Edison
        test = DS1X31Edison.DS1X31Edison(0x48, one_shot = True)

    elif sys.argv[1].lower() == 'raspberry':
        import DS1X31Raspberry
        test = DSiX31Raspberry.DS1X31Raspberry(0x48, one_shot = True)

    else:
        print "Unrecognized system! exiting..."
        exit()


test.init()
test.start()

# Get MAC id of device
mac_id = uuid.getnode()

print 'Temperature data being collected and sent to http://192.168.168.5:3000...'
while(True):
	temp = test.getTemp()
	unaware = datetime.now()
	tz = pytz.timezone('US/Eastern')
	now = tz.localize(unaware)
	r = requests.post('http://192.168.168.5:3000/temp', data = {'mac_id': mac_id, 'temp': temp, 'timestamp': now.strftime('%Y-%m-%dT%H:%M:%S%z')})
        time.sleep(10)
