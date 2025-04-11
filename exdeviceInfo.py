instance_name = 'testpi'
#instance_name = 'mobilepi'
#instance_name = 'bedroompi'
#instance_name = 'bathroompi'
#instance_name = 'kitchenpi'

debug_lvl = 1
# TRACE
# DEBUG
# INFO
# WARN
# ERROR
# FATAL

bme280_sd = {
    "abme280": {
        'class_name':'aBME280',
        'responsiblePartyName': 'abhik',
        'instanceName': instance_name,
        'manufacturer': 'Bosch',
        'deviceName': "bme280", 
        'sensors': {
            'temp-c': {
                'hz': 2**0,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz0', 'temp-c!float32!float32!afloat8']
            },
            'relativeHumidity': {
                'hz': 2**0,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz0', 'relativeHumidity!float32!float32!afloat5']
            },
            'pressure-pa': {
                'hz': 2**4,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz4', 'pressure-pa!int32!int32!aint']
            }
        }
    }
}

scd41_sd = {
    "ascd41": {
        'class_name':'aSCD41',
        'responsiblePartyName': 'abhik',
        'instanceName': instance_name,
        'manufacturer': 'Sensirion',
        'deviceName': "scd41",
        'sensors': {
            'temp-c': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'temp-c!float32!float32!afloat8']
            },
            'relativeHumidity': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'relativeHumidity!float32!float32!afloat5']
            },
            'co2-ppm': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'co2-ppm!int32!int32!aint']
            }
        }
    }
}

pmsa003i_sd = {
    "apmsa003i": {
        'class_name':'aPMSA003I',
        'responsiblePartyName': 'abhik',
        'instanceName': instance_name,
        'manufacturer': 'Plantower',
        'deviceName': "pmsa003i", 
        'sensors': {
            'envpm1um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm1um-ugperm3!int32!int32!aint']
            },
            'envpm2.5um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm2.5um-ugperm3!int32!int32!aint']
            },
            'envpm10um-ugperm3': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'envpm10um-ugperm3!int32!int32!aint']
            },
            'gtpm0.3um-per.1l': {
                'hz': 2**-2,
                'col_names': ['sampleDT!int64!datetime64[ns]!audelayhz-2', 'gtpm0.3um-per.1l!int32!int32!aint']
            },
        }
    }
}

i2c_sensor_descriptors = {} # add the element in the bme dict and the scd41 dict
i2c_sensor_descriptors.update(bme280_sd)
i2c_sensor_descriptors.update(scd41_sd)
i2c_sensor_descriptors.update(pmsa003i_sd)
