#alright so I'll be making a class??
# that takes in a dictonary????
# creates shared memory buffers for 1 seocnd of the data??
# and runs a loop to do all the specified io on the i2c bus???
# and spawns a writer for each of the sensors??


# the writer hasn't been written yet
# but it'll take a ctsb object of datatype
# with size nums samples in 2 seconds
# every second it will
# write every sample taken in the last second to a message thing for that day
# later it can even send the second to a server for live updates :0

# at the end of the day it'll spawn a process to convert the message thing to a df
#   it can spawn it at a random minute offset between 1 and 55
# the os will move all the df's at the end of the day + 1 hour

# the storage server will integrate the data into the dataset