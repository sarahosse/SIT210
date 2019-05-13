import time, smbus

# -- initialisations / variables --------------------------------------

# initialise I2C (System Management Bus, or SMBus)
i2cChannel = 1
BUS = smbus.SMBus(i2cChannel)

# TMP102 is a 7 bit address (left-shifted for read-write bit)
i2cAddress = 0x48

# 8-bit addresses of memory locations (or, registers)
TemperatureAddress = 0x00
ConfigurationAddress = 0x01

# -- function --------------------------------------------------------

# reads temp addresses in memory
# checks for negative temps (not really necessary in Summer...)
# calculates Celsius
def readTemperature():
    
    # read two temp registers
    readValue = BUS.read_i2c_block_data(i2cAddress, TemperatureAddress, 2)
    
    # low and high temps
    temperatureValue = (readValue[0] << 4)  (readValue[1] >> 5)
    
    # check if negative, and if so convert to two's complement    
    if (temperatureValue > 0x7FF):
        temperatureValue = temperatureValue - 4096
    
    # converts to Celcius
    tempCelcius = temperatureValue * 0.0625
    
    return tempCelcius


# -- continuously read temps ------------------------------------------

# print temp (to 2 digits) every ten seconds
while True:
    
    temp = readTemperature()
    
    print(round(temp, 2), " Celcius")
    
    time.sleep(10)
