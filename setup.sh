
#git clone https://github.com/AbhikChowdhury6/airQualPi.git ~/Documents/airQualPi

#remember to set the deviceInfo

#remember to enable i2c using raspi-config

#getting set up 
pip3 install icecream
pip3 install adafruit-circuitpython-scd4x
pip3 install adafruit-circuitpython-pm25
pip3 install adafruit-circuitpython-bme280
pip3 install adafruit-circuitpython-bme680
pip3 install lgpio

mkdir /home/pi/Documents/dayData
mkdir /home/pi/Documents/sensorData

crontab -e
#2 17 * * * /home/pi/miniforge3/envs/vision311/bin/python3.11 /home/pi/Documents/airQualPi/send.py
#1 * * * * /home/pi/miniforge3/envs/vision311/bin/python3.11 /home/pi/Documents/airQualPi/toDataFrames.py

#run using python main.py

