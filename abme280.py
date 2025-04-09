import torch.multiprocessing as mp
from datetime import datetime, timedelta, timezone
import torch
from zoneinfo import ZoneInfo
from bme280 import BME280
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from circularTimeSeriesBuffer import CircularTimeSeriesBuffers
from writeWorker import write_worker
import re
from icecream import ic

class sensor:
    def __init__(self, config, retrieve_data, dd, debug_lvl):
        print('starting sensor!')
        sys.stdout.flush()
        self.dd = dd
        self.retrieve_data = retrieve_data
        _ = retrieve_data() # a warmup reading
        self.hz = config['hz']
        self.delay_micros = 1_000_000/self.hz
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
        self.buffer = CircularTimeSeriesBuffers(self.hz, self.torch_dtype)

        self.write_exit_signal = torch.zeros(1, dtype=torch.int32).share_memory_()
        writeArgs = [self.buffer, self.dd, self.config['col_names'], self.debug_lvl, self.write_exit_signal]
        self.write_process = mp.Process(target=write_worker, args=((*writeArgs,)))
        self.write_process.start()

        self.retrive_after = datetime.fromtimestamp(0, tz=timezone.utc)
    
    def read_data(self):
        #check if it's the right time
        now = datetime.now().astimezone(ZoneInfo("UTC"))
        if now >= self.retrive_after:
            dm = self.delay_micros - (now.microsecond % self.delay_micros)
            self.retrive_after = now + timedelta(microseconds=dm)
            #print(now)
            #sys.stdout.flush()
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
        


class aBME280:
    def __init__(self, bus, descriptor, debug_lvl):
        print('starting a bme!')
        self.bme280 = BME280(i2c_dev=bus)
        def get_pressure_pa():
            return self.bme280.get_pressure() * 100
        
        retrieve_datas = {'temp-c': self.bme280.get_temperature,
                            'relativeHumidity': self.bme280.get_humidity,
                            'pressure-pa': get_pressure_pa}


        sensor_descriptors = descriptor['sensors']
        self.sensors = []
        for s in sensor_descriptors:
            dd = [descriptor['responsiblePartyName'],
                descriptor['instanceName'],
                descriptor['manufacturer'],
                'bme280',
                s,
                'internal']
            sen = sensor(sensor_descriptors[s], retrieve_datas[s], dd, debug_lvl)
            self.sensors.append(sen)

        