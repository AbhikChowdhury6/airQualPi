import adafruit_scd4x
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from sensor import Sensor


class aSCD41:
    def __init__(self, bus, descriptor, debug_lvl):
        print('starting a SCD41!')
        self.scd4x = adafruit_scd4x.SCD4X(bus)
        self.scd4x.start_periodic_measurement()

        self.is_ready = lambda: self.scd4x.data_ready
        
        self.get_co2 = lambda: self.scd4x.CO2
        self.get_temp = lambda: self.scd4x.temperature
        self.get_humidity = lambda: self.scd4x.relative_humidity
        
        retrieve_datas = {'temp-c': self.get_temp,
                            'relativeHumidity': self.get_humidity,
                            'co2-ppm': self.get_co2}


        sensor_descriptors = descriptor['sensors']
        self.sensors = []
        for s in sensor_descriptors:
            dd = [descriptor['responsiblePartyName'],
                descriptor['instanceName'],
                descriptor['manufacturer'],
                'scd41',
                s,
                'internal']
            sen = Sensor(sensor_descriptors[s], retrieve_datas[s], self.is_ready, dd, debug_lvl)
            self.sensors.append(sen)
