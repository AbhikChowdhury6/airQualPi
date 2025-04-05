from smbus2 import SMBus
import time
from datetime import datetime
from abme280 import aBME280

# at the end of the day it'll spawn a process to convert the message thing to a df
#   it can spawn it at a random minute offset between 1 and 55
# the os will move all the df's at the end of the day + 1 hour

# the storage server will integrate the data into the dataset

import importlib.util
import os

repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
classe_loc = repoPath + "airQualPi/"

def load_class_and_instantiate(filepath, class_name, *args, **kwargs):
    module_name = os.path.splitext(os.path.basename(filepath))[0]
    spec = importlib.util.spec_from_file_location(module_name, filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    
    tcls = getattr(module, class_name)
    instance = tcls(*args, **kwargs)
    return instance


# this is a process to be spawned
def I2C_BUS(bus_descriptor, debug_lvl, heart_beat, exitSignal):

    # init a bus using smbus2
    I2C_BUS = SMBus(1)
    sensors = []
    devices = []
    for device in bus_descriptor:
        newDevice = load_class_and_instantiate(
            classe_loc + device + '.py',
            bus_descriptor[device]['class_name'],
            I2C_BUS,
            bus_descriptor[device],
            debug_lvl
        )
        self.devices.append(newDevice)
        self.sensors = self.sensors + newDevice.sensors

    max_hz = max(s.hz for s in sensors)

    while True:
        pass
    # we'll have to instantiate an object for each device
    # those objects will spawn their writers on init
    # they'll pass back a list of get data functions, and the max update hz
    # and they'll pass back the write workers to check is alive on

    # we'll loop based on the max update hz of all the devices
    # when called they'll use the current timestamp to decide to 

    pass
