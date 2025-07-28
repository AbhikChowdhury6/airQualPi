
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

##air cap
#sudo nano /etc/systemd/system/aircap.service
#
#[Unit]
#Description=Run air cap in conda env
#After=network.target
#
#[Service]
#ExecStartPre=/usr/bin/rm -f /tmp/air_input
#ExecStartPre=/usr/bin/mkfifo /tmp/air_input
#ExecStart=/bin/bash -c "exec 3<>/tmp/air_input; /home/pi/miniforge3/envs/vision311/bin/python3.11 /home/pi/Documents/airQualPi/main.py <&3"
#WorkingDirectory=/home/pi/Documents/airQualPi
#User=pi
#Restart=on-failure
#StandardOutput=append:/home/pi/aircap.log
#StandardError=append:/home/pi/aircap.log
#
#[Install]
#WantedBy=multi-user.target
#vision
#
##to send q
#echo q > /tmp/air_input
#
## to start again
#sudo systemctl restart aircap.service