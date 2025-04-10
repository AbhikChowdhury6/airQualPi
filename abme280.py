from bme280 import BME280
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from sensor import Sensor


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
            sen = Sensor(sensor_descriptors[s], retrieve_datas[s], dd, debug_lvl)
            self.sensors.append(sen)

        