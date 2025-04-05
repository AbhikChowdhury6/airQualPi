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