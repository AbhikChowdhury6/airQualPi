from datetime import datetime, timedelta
from adafruit_pm25.i2c import PM25_I2C
import sys
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from sensor import Sensor


class aPMSA003I:
    def __init__(self, bus, descriptor, debug_lvl):
        print('starting a SCD41!')
        self.pm25 = PM25_I2C(bus, None)

        self.curr_data = 0
        self.fresh_till = 0
        #TODO figure out how to keep state and 
        self.is_ready = lambda: True
        
        self.get_envpm1um = lambda: self.aqdata["particles 03um"]
        self.get_envpm2p5um = lambda: self.aqdata["particles 03um"]
        self.get_envpm10um = lambda: self.aqdata["particles 03um"]
        self.get_gtpm0p3um = lambda: self.aqdata["particles 03um"]
        
        retrieve_datas = {'envpm1um-ugperm3': self.get_envpm1um,
                            'envpm2.5um-ugperm3': self.get_envpm2p5um,
                            'envpm10um-ugperm3': self.get_envpm10um,
                            'gtpm0.3um-per.1l': self.get_gtpm0p3um}


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
