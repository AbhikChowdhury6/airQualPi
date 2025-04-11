from adafruit_bme280 import basic as adafruit_bme280
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from sensor import Sensor


class aBME280:
    def __init__(self, bus, descriptor, debug_lvl):
        print('starting a bme!')
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(bus)
        
        self.is_ready = lambda: True

        self.get_temp_c = lambda: self.bme280.temperature
        self.get_elative_humidity = lambda: self.bme280.relative_humidity
        self.get_pressure_pa = lambda: self.bme280.pressure * 100
        
        retrieve_datas = {'temp-c': self.bme280.temperature,
                            'relativeHumidity': self.bme280.relative_humidity,
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
            sen = Sensor(sensor_descriptors[s], retrieve_datas[s], self.is_ready, dd, debug_lvl)
            self.sensors.append(sen)

        