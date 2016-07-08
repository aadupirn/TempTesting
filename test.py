import DS1X31
import time


test = DS1X31.DS1X31(0x48)

test.init()
test.start()

while True:
    print test.getTemp()
    time.sleep(1)
