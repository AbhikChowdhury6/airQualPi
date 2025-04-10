import time
import board
import adafruit_scd4x

i2c = board.I2C()
scd4x = adafruit_scd4x.SCD4X(i2c)

scd4x.start_periodic_measurement()
#print("Serial number:", [hex(i) for i in scd4x.serial_number])

while True:
    if scd4x.data_ready:
        print("CO2:", scd4x.CO2, "PPM")
        print("Temperature:", scd4x.temperature, "°C")
        print("Humidity:", scd4x.relative_humidity, "%rH")
    else:
        print("Waiting for data...")
    time.sleep(1)