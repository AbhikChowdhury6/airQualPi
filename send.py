# send all the parquet.gzips

#process for setting up remote user
# as root
# useradd -m uploadingGuest
# passwd <strong password here>
# as uploadingGuest
# mkdir recentSensorCap
# chmod 777 recentSensorCap

#process for setting up local
# ssh-keygen -t rsa
# ssh-copy-id uploadingGuest@192.168.1.113
# chrontab -e 
# add the line 0 3 * * * /home/$USER/Documents/videoProcessing/send.sh
# for logs check /var/log/syslog or /var/log/cron

#on pi
#2 17 * * * /home/pi/miniforge3/envs/vision/bin/python3.12 /home/pi/Documents/airQualPi/send.py
#1 * * * * /home/pi/miniforge3/envs/vision/bin/python3.12 /home/pi/Documents/airQualPi/toDataFrames.py


#on server
#8 17 * * * /usr/bin/mv /home/uploadingGuest/recentSensorCap/* /home/chowder/Documents/recentSensorCap/

import os
import subprocess
import sys
from datetime import datetime, timezone
import tzlocal
import logging
import logging.handlers

logger = logging.getLogger('sensor-uploader')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename="/home/" + os.getlogin() + '/sensor-uploader.log')
formatter = logging.Formatter('%(asctime)s - %(name)s: %(levelname)s: %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

print(f"the time started is {datetime.now()}")
# logger.info(f"the time started is {datetime.now()}")

serverip = "192.168.20.64"

pathToCollectedData = "/home/" + os.getlogin() + "/Documents/sensorData/"

foldersInCollectedData = sorted(os.listdir(pathToCollectedData))
if len(foldersInCollectedData) == 0:
    print("no files found, exiting")
    logger.info("no files found, exiting")
    sys.exit()



nameOfTodaysExtension =  datetime.now(timezone.utc).strftime("%Y-%m-%d%z")

startTime = datetime.now()
for folderName in foldersInCollectedData:
    #if you also want to send todays folder then add any argument when calling send
    if folderName.split('_')[-1] == nameOfTodaysExtension and len(sys.argv) == 1:
        continue
    source = pathToCollectedData + folderName
    
    # send the folder over
    print(f"starting send of {folderName}")
    logger.info(f"starting send of {folderName}")
    o = subprocess.run(["scp", "-r", source, "uploadingGuest@" + serverip +
                         ":/home/uploadingGuest/recentSensorCap/"],
                         capture_output=True)
    print(f"the returncode for uploading the direcotry was {o.returncode}")
    logger.info(f"the returncode for uploading the direcotry was {o.returncode}")
    
    # make it writeable by other users since the umask in the .bashrc isn't working for some reason
    o2 = subprocess.run(["ssh", "uploadingGuest@"  + serverip, "chmod", "-R", "777", 
                        "/home/uploadingGuest/recentSensorCap/" + folderName + "/"], 
                        capture_output=True)
    print(f"the returncode for upating the permissions was {o2.returncode}")
    logger.info(f"the returncode for upating the permissions was {o2.returncode}")


    #delete the folder locally if the send was successful
    if o.returncode == 0:
        print(f"successfuly sent now deleting {source}")
        logger.info(f"successfuly sent now deleting {source}")
        o = subprocess.run(["rm", "-r", source], capture_output=True)
        print("deleted") if o.returncode == 0 else print(o)
        logger.info("deleted") if o.returncode == 0 else logger.info(o)
    else:
        print(f"there was a problem sending {source} not deleting")
        logger.error(f"there was a problem sending {source} not deleting")
        print(o)
        logger.error(o)

print(f"done sending in {datetime.now() - startTime}!")
logger.info(f"done sending in {datetime.now() - startTime}!")
print(f"the time completed is {datetime.now()}")
# logger.info(f"the time completed is {datetime.now()}")
