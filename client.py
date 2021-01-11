# UDP client that requests time synchs from server

import socket
import sys
import time

# Track global variable, current simulated time
currSimTime = -1

def printTimeAfterSync():
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    print(  "time after update is:\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )

def printTimeBeforeSync():
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    print(  "time before update is:\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )


IP = "127.0.0.1"    # Server's IP
PORT = 2001 # Server's port

skew = 2
drift = 10

queryPeriod = skew / (2 * drift)
sleepTime = queryPeriod

address = (IP, PORT)

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )

sysTimeAfterSync = time.time()  # Store system time after sync

currSimTime = time.time() + skew    # Initialize current simulated time with skew

printTimeAfterSync()    # Initial output

time.sleep(sleepTime) # Wait queryPeriod seconds

sysTimeBeforeSync = time.time() # Store system time before sending sync request

currSimTime += (sysTimeBeforeSync - sysTimeAfterSync) * (1 + drift)  # Calculate current simulated time

printTimeBeforeSync()   # Print simulated time before sending sync request

sock.sendto(b"sync_req", address)   # Send sync request to server

# Receive server time message
data, addr = sock.recvfrom(1024)
serverTime = float(data.decode() )   # Get server time from data

# Calculate current simulated time
sysTimeAfterSync = time.time() # Update system time after sync
realRoundTripTime = sysTimeAfterSync - sysTimeBeforeSync
simRoundTripTime = realRoundTripTime * (1 + drift)
currSimTime = serverTime + simRoundTripTime / 2

printTimeAfterSync()   # Print simulated time after syncing

sleepTime = queryPeriod - realRoundTripTime    # Adjust the query period to account for round-trip time delay
