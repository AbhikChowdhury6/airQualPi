#air cap
sudo nano /etc/systemd/system/aircap.service

[Unit]
Description=Run air cap in conda env
After=network.target

[Service]
ExecStartPre=/usr/bin/rm -f /tmp/air_input
ExecStartPre=/usr/bin/mkfifo /tmp/air_input
ExecStart=/bin/bash -c "exec 3<>/tmp/air_input; /home/pi/miniforge3/envs/vision311/bin/python3.11 /home/pi/Documents/airQualPi/main.py <&3"
WorkingDirectory=/home/pi/Documents/airQualPi
User=pi
Restart=on-failure
StandardOutput=append:/home/pi/aircap.log
StandardError=append:/home/pi/aircap.log

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload
sudo systemctl enable aircap.service
sudo systemctl start aircap.service


#to send q
echo q > /tmp/air_input

# to start again
sudo systemctl restart aircap.service




git clone https://github.com/AbhikChowdhury6/airQualPi.git ~/Documents/airQualPi

remember to set the deviceInfo

remember to enable i2c using raspi-config

getting set up 
pip install icecream
pip3 install adafruit-circuitpython-scd4x
pip3 install adafruit-circuitpython-pm25
pip3 install adafruit-circuitpython-bme280
pip3 install lgpio

mkdir /home/pi/Documents/sensorData

crontab -e
2 17 * * * /home/pi/miniforge3/envs/vision311/bin/python3.12 /home/pi/Documents/airQualPi/send.py
1 * * * * /home/pi/miniforge3/envs/vision311/bin/python3.12 /home/pi/Documents/airQualPi/toDataFrames.py





Alright some new notes about the process of adding another sensor type
TODO
- make a new file (ascd41.py) and class (aSCD41) for the new sensor 
- figure out how to get the write code to work with the SMBUS i2c bus
- repeat the sensor and read data functions, but moudularize it more

a few whitngs to do
- implement a way for read data to check if the data is ready
- handle hz less than 1

so now the bme 280 capture is working!

lets make the 2 cron jobs

let's make a new flow to keep it separate from the video processing
on the pi
a folder called sensorData
in it files like dd_dayDesctiptor

the send works just like the other one

lets test send
alright so the only thongs left to do are the hourly and 


so some notes on main
- let's do a thing where we start with two sets of classes, actually 3 with the presence model

lets start with i2c
the object defintion would look something like this
sensors
{
    "abme280": {
        'class_name':' aBME280
        'responsiblePartyName': 'abhik',
        'instanceName': 'testing',
        'manufacturer': 'Bosch',
        'sensors': {
            'temp-c': {
                'hz': 1,
                'col_names': ['temp-c!float32'],
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0

            },
            'relativeHumidity': {
                'hz': 1,
                'col_names': ['relativeHumidity!float32'],
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            },
            'pressure-pa': {
                'hz': 16,
                'col_names': ['pressure-pa!int32'],
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            },
        }
    }
}

outputs
{
    "ssd1306_testing": {
        'responsiblePartyName': 'abhik',
        'manufacturer': 'adafruit',
        'outputs': {
            'screen': {
                'recording_vid': int32 mem obj init at 0,
                'recording_audio': int32 mem obj init at 0,
                'screen_switch': int32 mem obj init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            }
        }
    }
}



the cam object could look something like this
remember only add params I would immediately like to configure or are needed for addressing
{
    'deviceName_instanceName':{
        'responsiblePartyName': 'abhik',
        'manufacturer': 'abhik',
        'sensors': {
            'video': {
                'col_names': ['vid-idx!int32'],
                'presence': int32 mem obj init at 0,
                'cam_switch': int32 mem obj init at 0,
                'detect_img': int8 mem obj of size 480x360x3 init at 0,
                'recording_vid': int32 mem obj init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            }
        }
    }
}

we can just modify the vid write worker to do this writing
for the model
{
    'deviceName-yoloPerson_instanceName':{
        'responsiblePartyName': 'abhik',
        'manufacturer': 'ultralytics',
        'sensors': {
            'presence': {
                'col_names': ['presence-bool!int32'],
                'model': 'yolo11x.pt'
                'noRecTresh': 8
                'presence': int32 mem obj init at 0,
                'detect_img': int8 mem obj of size 480x360x3 init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            }
        }
    }
}

for the gpio
{
    'switch_instanceName':{
        'responsiblePartyName': 'abhik',
        'manufacturer': 'unknown',
        'sensors': {
            'cam_switch': {
                'plus_pin': X,
                'sense_pin': X,
                'gnd_pin': X,
                'cam_switch': int32 mem obj init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            },
            'audio_switch': {
                'plus_pin': X,
                'sense_pin': X,
                'gnd_pin': X,
                'audio_switch': int32 mem obj init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            },
            'screen_switch': {
                'plus_pin': X,
                'sense_pin': X,
                'gnd_pin': X,
                'screen_switch': int32 mem obj init at 0,
                'debug_lvl': int32 mem obj init at 0,
                'end-signal': int32 mem obj init at 0,
                'uptime': int32 mem obj init at 0
            }
        }
    }
}


alright so I'll get started with the BME280 I have and ya know try out a couple of handy new things as
I make a new pipeline