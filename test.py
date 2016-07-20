import DS1X31Edison
import time


test = DS1X31Edison.DS1X31Edison(0x48)

test.init()
test.start()

while True:
    print test.getTemp()
    time.sleep(1)
