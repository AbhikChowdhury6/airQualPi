import torch.multiprocessing as mp

from bme280 import BME280
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from circularTimeSeriesBuffer import CircularTimeSeriesBuffers
from writeWorker import write_worker


def getDtype(config):
    return config['col_names'][0].split('!')[1]


class aBME280:
    def __init__(self, descriptor):
        self.bme280 = BME280(i2c_dev=bus)
        sensor_descriptors = descriptor['sensors']

        #init temp
        config = sensor_descriptors['temp-c']
        ctsb = CircularTimeSeriesBuffers(config['hz'], getDtype(config))

        #init humidity


        #init pressure


        # init a ctsb
        ctsb = CircularTimeSeriesBuffers()
        # start a writer
    
    def read_temperature(self):
        return self.bme280.get_temperature()

    def read_pressure(self):
        return self.bme280.get_pressure()

    def read_humidity(self):
        return self.bme280.get_humidity()
