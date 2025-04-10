import adafruit_scd4x
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from sensor import Sensor


class aSCD41:
    def __init__(self, bus, descriptor, debug_lvl):
        print('starting a SCD41!')
        self.scd4x = adafruit_scd4x.SCD4X(i2c)
        self.scd4x.start_periodic_measurement()
        
        self.get_co2 = lambda: self.scd4x.read_measurement()[0]
        self.get_temp = lambda: self.scd4x.read_measurement()[1]
        self.get_humidity = lambda: self.scd4x.read_measurement()[2]
        
        retrieve_datas = {'temp-c': self.get_temp,
                            'relativeHumidity': self.get_humidity,
                            'co2-ppm-pa': self.get_co2}


        sensor_descriptors = descriptor['sensors']
        self.sensors = []
        for s in sensor_descriptors:
            dd = [descriptor['responsiblePartyName'],
                descriptor['instanceName'],
                descriptor['manufacturer'],
                'scd41',
                s,
                'internal']
            sen = sensor(sensor_descriptors[s], retrieve_datas[s], dd, debug_lvl)
            self.sensors.append(sen)
