from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo
import time

import torch
import torch.multiprocessing as mp

import sys
from icecream import ic

import re


repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from circularTimeSeriesBuffer import CircularTimeSeriesBuffers
from writeWorker import write_worker

def secs_since_midnight(dt):
    return (dt - dt.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()

class Sensor:
    def __init__(self, config, retrieve_data, is_ready, dd, debug_lvl):
        print('starting sensor!')
        sys.stdout.flush()
        self.dd = dd
        self.hz = config['hz']
        self.delay_micros = int(1_000_000/self.hz)
        self.config = config
        self.torch_dtype = getattr(torch, config['col_names'][1].split('!')[1])
        self.pandas_dtype = config['col_names'][1].split('!')[2]
        self.abc1_dtype = config['col_names'][1].split('!')[3]
        matches = re.findall(r'-?\d+', self.abc1_dtype)
        self.rounding_bits = int(matches[-1]) if matches else 0
        self.billionths = 1_000_000_000/(2**self.rounding_bits)
        self.debug_lvl = debug_lvl

        #print(self.hz, self.dtype)
        #sys.stdout.flush()
        buff_len = self.hz if self.hz > 1 else 1
        self.buffer = CircularTimeSeriesBuffers(buff_len, self.torch_dtype)

        self.write_exit_signal = torch.zeros(1, dtype=torch.int32).share_memory_()
        writeArgs = [self.buffer, self.dd, self.config['col_names'], self.debug_lvl, self.write_exit_signal]
        self.write_process = mp.Process(target=write_worker, args=((*writeArgs,)))
        self.write_process.start()

        self.retrive_after = datetime.fromtimestamp(0, tz=timezone.utc)

        self.is_ready = is_ready
        self.retrieve_data = retrieve_data
        while not self.is_ready():
            print("Waiting for data...")
            time.sleep(self.delay_micros/1_000_000)
        _ = self.retrieve_data() # a warmup reading
    
    def read_data(self):
        # i'd like it to automatically wait till the rounded hz seconds
        # up to 128 seconds
        # calc the offset seconds from the start of the day

        #check if it's the right time
        now = datetime.now().astimezone(ZoneInfo("UTC"))

        # wait till the rounded hz seconds 
        if self.hz < 1 and int(secs_since_midnight(now)) % int(self.delay_micros/1_000_000) != 0:
            return

        if now >= self.retrive_after:
            #wait till the next timestep
            dm = self.delay_micros - (now.microsecond % self.delay_micros)
            self.retrive_after = now + timedelta(microseconds=dm)

            if not self.is_ready():
                return
            
            #round ts
            if self.hz <= 1:
                now = now.replace(microsecond=0)
            else:
                rounded_down_micros = (now.microsecond//self.delay_micros) * self.delay_micros
                now = now.replace(microsecond=int(rounded_down_micros))

            new_data = self.retrieve_data()
            
            if self.rounding_bits == 0:
                self.buffer.append(int(new_data), now)
                return 

            #ic(new_data)
            #sys.stdout.flush()
            #we need 5 didgits to prefecly define afloat 5 and same for 6 and 7 and 8
            # honestly let's just handle up to 9 bits of rounding for now and that should even cover our quats ok
            
            rounded_data = int(new_data)
            this_billionths = int((new_data%1) * 1_000_000_000)
            floord =  (this_billionths // self.billionths)  *  self.billionths
            error =  this_billionths - floord
            
            if error >= self.billionths/2:
                rounded_data += (floord + self.billionths)/1_000_000_000
            else:
                rounded_data += floord/1_000_000_000
            
            #ic(this_billionths, floord, error)
            #ic(rounded_data)
            
            self.buffer.append(rounded_data, now)
        
