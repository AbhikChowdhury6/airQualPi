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



class sensor:
    def __init__(self, config, retrieve_data, dd, debug_lvl):
        print('starting sensor!')
        sys.stdout.flush()
        self.dd = dd
        self.retrieve_data = retrieve_data
        self.hz = config['hz']
        self.delay_micros = 1_000_000/self.hz
        self.config = config
        self.dtype = getattr(torch, config['col_names'][0].split('!')[1])
        self.debug_lvl = debug_lvl

        #print(self.hz, self.dtype)
        #sys.stdout.flush()
        self.buffer = CircularTimeSeriesBuffers(self.hz, self.dtype)

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
            #print(new_data)
            #sys.stdout.flush()
            self.buffer.append(new_data, now)
        


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

        