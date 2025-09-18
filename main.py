from datetime import datetime
import time
import torch
import torch.multiprocessing as mp
import select

import sys
import os
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from i2cController import I2C_BUS
if os.path.exists(repoPath + "airQualPi/deviceInfo.py"):
    from deviceInfo import debug_lvl, i2c_sensor_descriptors
else:
    print('no device config found. exiting')
    sys.exit()


exit_signal = torch.zeros(1, dtype=torch.int32).share_memory_()

i2c_process = mp.Process(target=I2C_BUS, args=(i2c_sensor_descriptors, debug_lvl, exit_signal))
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

    print(f"i2c proccess is {processes[0].is_alive()}")


    if select.select([sys.stdin], [], [], 0)[0]:
        if sys.stdin.read(1) == 'q':
            print("got q going to start exiting")
            exit_signal[0] = 1
            break
    time.sleep(1)

print('waiting 5 seconds for subprocesses to exit')
time.sleep(5)
print('exiting now')