import torch.multiprocessing as mp
from datetime import datetime, timedelta

from bme280 import BME280
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from circularTimeSeriesBuffer import CircularTimeSeriesBuffers
from writeWorker import write_worker



class sensor:
    def __init__(self, config, retrieve_data, dd, debug_lvl):
        self.dd = dd
        self.retrieve_data = retrieve_data
        self.hz = config['hz']
        self.delay = timedelta(seconds=(1/self.hz))
        self.config = config
        self.dtype = config['col_names'][0].split('!')[1]
        self.debug_lvl = debug_lvl

        self.buffer = CircularTimeSeriesBuffers(self.hz, self.dtype)

        self.write_exit_signal = torch.zeros(1, dtype=torch.int32).share_memory_()
        writeArgs = [self.buffer, self.dd, self.config['col_names'], self.debug_lvl, self.write_exit_signal]
        self.write_process = mp.Process(target=write_worker, args=(*writeArgs))
        self.write_process.start()

        self.retrive_after = datetime.fromtimestamp(0, tz=timezone.utc)
    
    def read_data(self):
        #check if it's the right time
        now = datetime.now().astimezone()
        if now >= self.retrive_after:
            self.retrive_after = now + self.delay
            self.buffer.append(now, self.retrieve_data())
        


class aBME280:
    def __init__(self, bus, descriptor, debug_lvl):
        self.bme280 = BME280(i2c_dev=bus)
        retrieve_datas = {'temp-c': self.bme280.get_temperature,
                            'relativeHumidity': self.bme280.get_humidity,
                            'pressure-pa': self.bme280.get_pressure}


        sensor_descriptors = descriptor['sensors']
        self.sensors = []
        for s in sensor_descriptors:
            dd = [descriptor['responsiblePartyName'],
                descriptor['instanceName'],
                descriptor['manufacturer'],
                'bme280',
                s,
                'internal']
            sensor = sensor(sensor_descriptors[s], retrieve_datas[s], dd, debug_lvl)
            sensors.append(sensor)

        