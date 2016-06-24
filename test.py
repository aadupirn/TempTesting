import DS1X31
import time

test = DS1X31.DS1X31(0x48)

test.init()
test.start()

for x in range(50):
	print test.getTemp()
        time.sleep(.5)
