import time
from datetime import datetime


keys = ["responsiblePartyName", "instanceName", "developingPartyName", "deviceName", "dataType", "dataSource"]
# what are my descriptors going to look like?
['abhik', 'testing', 'Bosch', 'BME280', 'airTemp-C', 'internal']
['abhik', 'testing', 'Bosch', 'BME280', 'relativeHumidity', 'internal']
['abhik', 'testing', 'Bosch', 'BME280', 'pressure-hpa', 'internal']



# this file will just
# start up an i2cbus and pass in the sensors dict
# later we can figure out how to do the outs.



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
