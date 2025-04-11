# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

import time
from datetime import datetime
import board
from adafruit_bme280 import basic as adafruit_bme280

# Create sensor object, using the board's default I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller
bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c,  address=0x76)

# OR create sensor object, using the board's default SPI bus.
# import digitalio
# spi = board.SPI()
# bme_cs = digitalio.DigitalInOut(board.D10)
# bme280 = adafruit_bme280.Adafruit_BME280_SPI(spi, bme_cs)

# change this to match the location's pressure (hPa) at sea level
delay_micros = 1_000_000/16

time.sleep(1 - datetime.now().microsecond/1_000_000)
while True:
    print(f"{datetime.now()} Pressure: {bme280.pressure:.2f} hPa")
    micros_to_delay = delay_micros - (datetime.now().microsecond % delay_micros)
    time.sleep(micros_to_delay/1_000_000)
