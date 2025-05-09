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
# lierally unbundle it if there's any difference in sample rate8
# also just unbundle everything that won't usually be used together

#package 1 sec of updates and send it to write or over the network


# why do i even need a main loop?, ah yes to make sure my busses are ok
# so yes, all this file will handle is using the busses to grab data (and write it in case of the screen)
# I wish the captures could happen in parallel for every interface too
#   camera
#   i2c
#   spi 



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
