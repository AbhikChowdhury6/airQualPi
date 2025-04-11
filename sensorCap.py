import time
import sys
import torch
import select
from datetime import datetime
import torch.multiprocessing as mp
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")

from i2cController import I2C_BUS

debug_lvl = int(sys.argv[1])
# TRACE
# DEBUG
# INFO
# WARN
# ERROR
# FATAL


i2c_sensor_descriptor = {
    "abme280": {
        'class_name':'aBME280',
        'responsiblePartyName': 'abhik',
        'instanceName': 'testing',
        'manufacturer': 'Bosch',
        'sensors': {
            'temp-c': {
                'hz': 2**0,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz0', 'temp-c!float32!float32!afloat8']
            },
            'relativeHumidity': {
                'hz': 2**0,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz0', 'relativeHumidity!float32!float32!afloat5']
            },
            'pressure-pa': {
                'hz': 2**4,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz4', 'pressure-pa!int32!int32!aint']
            }
        }
    }, 
    "ascd41": {
        'class_name':'aSCD41',
        'responsiblePartyName': 'abhik',
        'instanceName': 'testing',
        'manufacturer': 'Sensirion',
        'sensors': {
            'temp-c': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'temp-c!float32!float32!afloat8']
            },
            'relativeHumidity': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'relativeHumidity!float32!float32!afloat5']
            },
            'co2-ppm': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'co2-ppm!int32!int32!aint']
            }
        }
    }, 
    "apmsa003i": {
        'class_name':'aPMSA003I',
        'responsiblePartyName': 'abhik',
        'instanceName': 'testing',
        'manufacturer': 'Plantower',
        'sensors': {
            'envpm1um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm1um-ugperm3!int32!int32!aint']
            },
            'envpm2.5um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm2.5um-ugperm3!int32!int32!aint']
            },
            'envpm10um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm10um-ugperm3!int32!int32!aint']
            },
            'gtpm0.3um-per.1l': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'gtpm0.3um-per.1l!int32!int32!aint']
            },
        }
    }
}


#environmental envpm1um-ugperm3, envpm2.5um-ugperm3, envpm10um-ugperm3, pm0.3um-per.1L

# this file will just
# start up an i2cbus and pass in the sensors dict
# later we can figure out how to do the outs.
exit_signal = torch.zeros(1, dtype=torch.int32).share_memory_()

i2c_process = mp.Process(target=I2C_BUS, args=(i2c_sensor_descriptor, debug_lvl, exit_signal))
i2c_process.start()

processes = {}
processes['i2c_process'] = i2c_process

# make sure my processes are alive, and if I recive q exit everything
while True:
    if any(not processes[p].is_alive() for p in processes):
        for p in processes:
            print(p, processes[p].is_alive())
        exit_signal[0] = 1
        break


    if select.select([sys.stdin], [], [], 0)[0]:
        if sys.stdin.read(1) == 'q':
            print("got q going to start exiting")
            exit_signal[0] = 1
            break
    time.sleep(1)

print('waiting 5 seconds for subprocesses to exit')
time.sleep(5)
print('exiting now')