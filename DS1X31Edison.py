import mraa

class DS1X31Edison:

        # Set up static bit masks
        one_shot_cfg = 0x01
        polarity_cfg = 0x02
        res0_cfg = 0x04
        res1_cfg = 0x08
        
        # Define the commands
        START_CONVERT = 0x51 # Start/trigger conversion 
        STOP_CONVERT = 0x22  # Stop conversion if device is in continuous mode
        READ_TEMP = 0xAA     # reads last converted temp from 2 byte temp register
        ACCESS_TH = 0xA1     # read/write the 2 byte high temp alarm register
        ACCESS_TL = 0xA2     # read/write the 2 byte low temp alarm register
        ACCESS_CFG = 0xAC    # read/write config byte
        RESET = 0x54         # Simulates power cycle

        # Define smbus object
        bus = mraa.I2c(6)

        def __init__(self, address, one_shot=False, res0=True, res1=True, polarity=False):
                self.address = address
                self.one_shot = one_shot
		self.res0 = res0
		self.res1 = res1
                self.polarity = polarity

        # Function to initialize device
        def init(self):
                #generate configuration bit
                cfg_byte = 0x00
                if(self.one_shot):
                        cfg_byte = cfg_byte | self.one_shot_cfg
                if(self.res0):
                        cfg_byte = cfg_byte | self.res0_cfg
                if(self.res1):
                        cfg_byte = cfg_byte | self.res1_cfg
                if(self.polarity):
                        cfg_byte = cfg_byte | self.polarity_cfg

                # Set up i2c
                self.bus.address(self.address)
                self.bus.writeReg(self.ACCESS_CFG, cfg_byte)

               
        # Start conversion if in continous mode, or trigger
        # conversion if in one shot mode
        def start(self):
                self.bus.writeByte(self.START_CONVERT)

        # Stop conversion if in continous mode
        def stop(self):
                self.bus.writeByte(self.STOP_CONVERT)

        # Get temperature reading, pass 'c' for celsius
        def getTemp(self, unit='f'):

                # If in one shot mode, trigger conversion
                if (self.one_shot):
                        self.bus.writeByte(self.START_CONVERT)

                result = self.bus.readWordReg(self.READ_TEMP)
		whole = (result & 0xFF)
		fraction = (((result >> 8) & 0xFF )>>4)/16.0  #build fraction part of temperature
	        out = whole + fraction		#add whole to fraction
		return self.__CtoF(out) if unit == 'f' else out

        # Private function to convert C to F
        def __CtoF(self, celsius):
                return (celsius * (9.0/5.0)) + 32.0
