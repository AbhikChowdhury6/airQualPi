from smbus2 import SMBus
import time
from datetime import datetime
from abme280 import aBME280
#alright so I'll be making a class??
# that takes in a dictonary????
# creates shared memory buffers for 1 seocnd of the data??
# and runs a loop to do all the specified io on the i2c bus???
# and spawns a writer for each of the sensors??


# the writer hasn't been written yet
# but it'll take a ctsb object of datatype
# with size nums samples in 2 seconds
# every second it will
# write every sample taken in the last second to a message thing for that day
# later it can even send the second to a server for live updates :0

# at the end of the day it'll spawn a process to convert the message thing to a df
#   it can spawn it at a random minute offset between 1 and 55
# the os will move all the df's at the end of the day + 1 hour

# the storage server will integrate the data into the dataset

# we also don't have to complicate things yet by solving the each field
# per sensorwe could just define a new object with all the data it needs

def I2C_BUS(bus_descriptor, debug_lvl, heart_beat, exitSignal):

    # init a bus using smbus2
    I2C_BUS = SMBus(1)
    sesnors = []
    for device in bus_descriptor
    sensors.append()

    # we'll have to instantiate an object for each device
    # those objects will spawn their writers on init
    # they'll pass back a list of get data functions, and the max update hz
    # and they'll pass back the write workers to check is alive on

    # we'll loop based on the max update hz of all the devices
    # when called they'll use the current timestamp to decide to 

    pass
