from smbus2 import SMBus
import time
from datetime import datetime, timedelta

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
def I2C_BUS(bus_descriptor, debug_lvl, exitSignal):

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
        self.sensors += newDevice.sensors


    min_delay = min(s.delay for s in sensors)  # timedelta object
    delay_secs = min_delay.total_seconds()

    # Align to the next full second
    now = datetime.now()
    aligned_start = now.replace(microsecond=0) + timedelta(seconds=1)
    time_to_sleep = (aligned_start - now).total_seconds()
    time.sleep(time_to_sleep)

    # Start loop
    next_time = datetime.now()
    while True:
        for sensor in sensors:
            sensor.read_data()
        
        if exitSignal[0]:
            print('sending write exit signals to i2c sensors')
            for sensor in sensors:
                sensor.write_exit_signal = 1
            break

        # Set next time, aligned to the delay grid
        next_time += min_delay
        now = datetime.now()
        sleep_duration = (next_time - now).total_seconds()

        if sleep_duration > 0:
            time.sleep(sleep_duration)
        else:
            if debug_lvl > 0:
                print(f"[WARNING] Loop overran by {-sleep_duration:.3f} seconds")
            next_time = datetime.now()  # Reset so drift doesn't accumulate
        
print('i2c waiting 3 seconds for writers to exit')
time.sleep(3)
print('i2c exiting')  



