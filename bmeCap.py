import time
from datetime import datetime
from smbus2 import SMBus
from bme280 import BME280

# Initialize the I2C bus
I2C_BUS = SMBus(1)

# Base Sensor Class
class Sensor:
    """Generic sensor class to manage update rate and next read time."""
    def __init__(self, name, ur, get_latest_val):
        self.name = name
        self.update_rate = ur  # Hz
        self.nrt = 0  # Next Read Time (subsecond index)
        self.get_latest_val = get_latest_val  # Function to get sensor data

    def should_update(self, subsec_idx):
        """Check if it's time to update this sensor."""
        return subsec_idx % (max_rate // self.update_rate) == 0

# Device Manager Class for BME280
class BME280Device:
    """Handles BME280 sensor communication."""
    def __init__(self, bus):
        self.bme280 = BME280(i2c_dev=bus)

    def read_temperature(self):
        return self.bme280.get_temperature()

    def read_pressure(self):
        return self.bme280.get_pressure()

    def read_humidity(self):
        return self.bme280.get_humidity()

# Initialize Device Instance
bme280_device = BME280Device(I2C_BUS)

# Sensor Objects with Update Rates
sensors = [
    Sensor("bme280_temp", 1, bme280_device.read_temperature),  # 1 Hz
    Sensor("bme280_humidity", 1, bme280_device.read_humidity), # 1 Hz
    Sensor("bme280_pressure", 32, bme280_device.read_pressure) # 32 Hz
]

keys = ["responsiblePartyName", "instanceName", "developingPartyName", "deviceName", "dataType", "dataSource"]
# what are my descriptors going to look like?
['abhik', 'testing', 'Bosch', 'BME280', 'airTemp-C', 'internal']
['abhik', 'testing', 'Bosch', 'BME280', 'relativeHumidity', 'internal']
['abhik', 'testing', 'Bosch', 'BME280', 'pressure-hpa', 'internal']

# for each of these objects I would like a circular time series buffer to separate the cap
# from the writing and filtering

# we could have the write worker process in the class too, now that's something to think about
# not to over optimize, but the polling on the writer/ send process to reduce latency is a question
# but let's just get the write process to check every second
# and let's get it to write the data to message pack
# at the end of the day let's covert it, in this case to a df, later to a .abc1, for each sensor
# and send it
# let's leave any packets unbundled (the only reason to bundle is to save on redifining time stamps)

# later if we have like IMU data that is entagled, we can bundle it
# 9 axis sensor readings seems alright
# or data where streams might affect other sensor readings?
# mpu6050 and temp? that seems like a bit much

#the only thing is that the abc1 codec so far doesn't really do sparsity that well
#lierally unbundle it if there's any difference in sample rate, that's the real takeaway 

#package 1 sec of updates and send it to write or over the network

# Determine the max update rate for loop timing
max_rate = max(sensor.update_rate for sensor in sensors)
loop_delay = 1 / max_rate

# Wait until a full second starts
while True:
    now = datetime.now()
    if now.microsecond < 1000:
        break
    time.sleep(0.001)

# Sampling loop
subsec_idx = 0
while True:
    now = datetime.now()

    # Read sensors at their scheduled times
    for sensor in sensors:
        if sensor.should_update(subsec_idx):
            value = sensor.get_latest_val()
            print(f"{sensor.name}: {value}")

    # Increment sub-second index and sleep
    subsec_idx = (subsec_idx + 1) % max_rate
    time.sleep(loop_delay)
