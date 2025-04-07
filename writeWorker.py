import torch
from datetime import datetime, timedelta, timezone
import time
import sys
import csv
repoPath = "/home/pi/Documents/"
sys.path.append(repoPath + "airQualPi/")
from circularTimeSeriesBuffer import CircularTimeSeriesBuffers

def write_worker(ctsb: CircularTimeSeriesBuffers, deviceDescriptor, colNames,
                   debug_lvl, exitSignal):
    # all this should do is save the last second
    def intTensorToDtList(tensor):
        return [datetime.fromtimestamp(ts_ns.item() / 1e9, tz=timezone.utc) for ts_ns in tensor]

    while True:
        st = datetime.now()
        secondsToWait = (1 - st.microsecond/1_000_000) + .0625 # 1/16 of a sec
        #print(f"writer: waiting {secondsToWait} till {st + timedelta(seconds=secondsToWait)}")
        time.sleep(secondsToWait)

        lastBuffNum = ((ctsb.bn[0] + (ctsb.numBuffs[0]-1)) % ctsb.numBuffs[0]).clone()

        if ctsb.lengths[lastBuffNum][0] == 0:
                continue
        
        newTimestamps = intTensorToDtList(ctsb.time_buffers[lastBuffNum][:ctsb.lengths[lastBuffNum][0]])
        day_file_name = '/home/pi/Documents/dayData' + "_".join(deviceDescriptor) + "_" +\
                        newTimestamps[0].strftime('%Y-%m-%d%z') + '.csv'
        
        # other popular types float64, int64, float32, int32
        headers = ['sampleDT!datetime64[ns]'] + colNames
        with open(day_file_name, "a", newline="") as f:
            writer = csv.writer(f)
            if not os.path.exists(day_file_name):  # Write headers only if file is new
                writer.writerow(headers)
            
            for i, data in enumerate(ctsb.data_buffers[lastBuffNum][:ctsb.lengths[lastBuffNum][0]]):
                writer.writerow([newTimestamps[i].isoformat()] + data)
        
        if exitSignal[0]:
            break
            
        #honestly we could just have a cron job clean up and do the pandas conversions
    print('exiting writer for ', "_".join(deviceDescriptor))
