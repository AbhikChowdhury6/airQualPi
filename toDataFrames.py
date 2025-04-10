#for every csv, trun it into a dataframe of the correct type
#add an hour field if needed
import os
import csv
import pandas as pd
from zoneinfo import ZoneInfo
from datetime import datetime, timezone
from icecream import ic

source = "/home/" + os.getlogin() + "/Documents/dayData/"

destination = "/home/" + os.getlogin() + "/Documents/sensorData/"
os.makedirs(destination, exist_ok=True)


#to to fnstring
def dt_to_fnString(dt):
    return dt.astimezone(ZoneInfo("UTC")).strftime('%Y-%m-%dT%H%M%S,%f%z')


curr_ext = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H%z') + ".csv"
# for every csv
csvs = sorted(os.listdir(source))
for file in csvs:
    if file.split('_')[-1] == curr_ext:
        continue
    # getting the first row of the csv that contains the header
    with open(source + file, newline="") as f:
        reader = csv.reader(f)
        headers = next(reader)

    # we're going to parse out the pandas data types
    pandas_dtypes = [s.split('!')[2] for s in headers]
    datetime_cols = [col for col, dtype in zip(headers, pandas_dtypes) if dtype == "datetime64[ns]"]
    dtype_map = {col: dtype for col, dtype in zip(headers, pandas_dtypes) if dtype != "datetime64[ns]"}
    ic(datetime_cols, dtype_map, pandas_dtypes)

    # read it in as a dataframe with the types
    df = pd.read_csv(
        source + file,
        skiprows=1,               # Skip the original header
        names=headers,
        dtype=dtype_map,
        parse_dates=datetime_cols
    )

    #set the index as sampleDT
    df = df.set_index(headers[0])
    df.index = pd.to_datetime(df.index, utc=True, format='ISO8601')
    ic(df.dtypes)
    ic(df.head())
    # each file is named with the first and last datetime
    firstTs = df.index[0]
    lastTs = df.index[-1]
    ic(firstTs)
    ic(type(firstTs))
    ic(lastTs)
    target_file_name = dt_to_fnString(firstTs) + '_' + dt_to_fnString(lastTs) + '.parquet.gzip'

    # save it to a folder with the name of the dd and date
    device_descriptor = file.split('_')[:-1]
    target_folder_name = "_".join(device_descriptor) + '_' + firstTs.strftime('%Y-%m-%d%z') +'/'
    os.makedirs(destination + target_folder_name, exist_ok=True)
    
    df.to_parquet(destination + target_folder_name + target_file_name, compression='gzip')
    print(f"wrote: {target_folder_name + target_file_name}")
    os.remove(source + file)

    

