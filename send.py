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

import argparse
import os
import subprocess
import sys
from datetime import datetime, timezone
import tzlocal
import logging
import logging.handlers

parser = argparse.ArgumentParser()
parser.add_argument("--include-today", action="store_true", help=(
    "Also send today's folder(s). Safe to run anytime: toDataFrames.py only "
    "ever writes a parquet.gzip here once its source hour's CSV is fully "
    "read (it explicitly skips the current hour), and never appends to a "
    "file after writing it -- so every file already in sensorData/ is a "
    "finished artifact, unlike piVidCap's in-progress new.mp4. Each file is "
    "sent and deleted individually as its own upload is confirmed; the "
    "folder itself is left in place so later hours can keep landing in it."
))
args = parser.parse_args()

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


def send_completed_folder(folderName, source):
    """Send a folder whose day is fully over, then delete it locally on success."""
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


def send_todays_completed_files(folderName, source):
    """Send whatever hourly files today's folder has produced so far, one at a time.

    Every file here is already a finished write (toDataFrames.py never revisits
    one after writing it), so there's nothing to exclude by name -- unlike
    piVidCap's new.mp4. A source file is only deleted once its own upload is
    confirmed, and the folder itself is left in place for later hours.
    """
    entries = sorted(f for f in os.listdir(source) if os.path.isfile(os.path.join(source, f)))
    if not entries:
        print(f"no completed files in {folderName} yet, nothing to send")
        logger.info(f"no completed files in {folderName} yet, nothing to send")
        return

    print(f"starting partial send of {folderName} ({len(entries)} completed files)")
    logger.info(f"starting partial send of {folderName} ({len(entries)} completed files)")
    remoteDir = "/home/uploadingGuest/recentSensorCap/" + folderName + "/"
    o = subprocess.run(["ssh", "uploadingGuest@" + serverip, "mkdir", "-p", remoteDir],
                        capture_output=True)
    if o.returncode != 0:
        print(f"could not create {remoteDir} on the server, aborting partial send")
        logger.error(f"could not create {remoteDir} on the server: {o}")
        return

    for fileName in entries:
        filePath = os.path.join(source, fileName)
        o = subprocess.run(["scp", filePath, "uploadingGuest@" + serverip + ":" + remoteDir],
                            capture_output=True)
        if o.returncode == 0:
            os.remove(filePath)
            print(f"  sent + removed {fileName}")
            logger.info(f"  sent + removed {fileName}")
        else:
            print(f"  problem sending {fileName}, not deleting")
            logger.error(f"  problem sending {fileName}: {o}")

    o2 = subprocess.run(["ssh", "uploadingGuest@" + serverip, "chmod", "-R", "777", remoteDir],
                        capture_output=True)
    print(f"the returncode for upating the permissions was {o2.returncode}")
    logger.info(f"the returncode for upating the permissions was {o2.returncode}")


startTime = datetime.now()
for folderName in foldersInCollectedData:
    source = pathToCollectedData + folderName
    if folderName.split('_')[-1] == nameOfTodaysExtension:
        if args.include_today:
            send_todays_completed_files(folderName, source)
        continue
    send_completed_folder(folderName, source)

print(f"done sending in {datetime.now() - startTime}!")
logger.info(f"done sending in {datetime.now() - startTime}!")
print(f"the time completed is {datetime.now()}")
# logger.info(f"the time completed is {datetime.now()}")
