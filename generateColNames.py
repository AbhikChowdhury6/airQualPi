import os
import csv


data_folder = "/home/pi/Documents/dayData/"

name_bases_and_columns = {
    "Sensirion_scd41_temp-c_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,temp-c!float32!float32!afloat8",
    "Sensirion_scd41_relativeHumidity_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,relativeHumidity!float32!float32!afloat5",
    "Sensirion_scd41_co2-ppm_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,co2-ppm!int32!int32!aint",
    "Bosch_bme280_temp-c_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,temp-c!float32!float32!afloat8",
    "Bosch_bme280_relativeHumidity_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,relativeHumidity!float32!float32!afloat5",
    "Bosch_bme280_pressure-pa_internal": "sampleDT!int64!datetime64[ns]!audelayhz4,pressure-pa!int32!int32!aint",
    "Bosch_bme680_temp-c_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,temp-c!float32!float32!afloat8",
    "Bosch_bme680_relativeHumidity_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,relativeHumidity!float32!float32!afloat5",
    "Bosch_bme680_pressure-pa_internal": "sampleDT!int64!datetime64[ns]!audelayhz4,pressure-pa!int32!int32!aint",
    "Bosch_bme680_voc-ohm_internal": "sampleDT!int64!datetime64[ns]!audelayhz0,voc-ohm!int32!int32!aint",
    "Plantower_pmsa003i_envpm1um-ugperm3_internal": "sampleDT!int64!datetime64[ns]!audelayhz-2,envpm1um-ugperm3!int32!int32!aint",
    "Plantower_pmsa003i_envpm2.5um-ugperm3_internal": "sampleDT!int64!datetime64[ns]!audelayhz-2,envpm2.5um-ugperm3!int32!int32!aint",
    "Plantower_pmsa003i_envpm10um-ugperm3_internal": "sampleDT!int64!datetime64[ns]!audelayhz-2,envpm10um-ugperm3!int32!int32!aint",
    "Plantower_pmsa003i_gtpm0.3um-per.1l_internal": "sampleDT!int64!datetime64[ns]!audelayhz-2,gtpm0.3um-per.1l!int32!int32!aint",
}

for file in os.listdir(data_folder):

    base_name = "_".join(file.split('_')[2:-1])  # manufacturer_device_sensor_internal

    file_path = os.path.join(data_folder, file)

    # check if the first column in the first line is a character
    try:
        with open(file_path, 'r', newline='') as f:
            reader = csv.reader(f)
            first_row = next(reader, [])
    except Exception:
        first_row = []

    needs_header = True
    if first_row and len(first_row) > 0 and isinstance(first_row[0], str):
        # treat as header present if first token looks non-numeric (starts with alpha) or contains '!'
        token = first_row[0].strip()
        if token and (token[0].isalpha() or '!' in token):
            needs_header = False

    if not needs_header:
        print(f"OK: {file} already has header")
        continue

    header_line = name_bases_and_columns.get(base_name)
    if not header_line:
        print(f"SKIP: No header mapping for {base_name} ({file})")
        continue

    # prepend the header line to the file
    with open(file_path, 'r', newline='') as f:
        existing = f.read()

    with open(file_path, 'w', newline='') as f:
        f.write(header_line + '\n')
        f.write(existing)
    print(f"FIXED: Prepended header for {file}")