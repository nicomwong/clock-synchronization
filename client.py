# UDP client that requests time synchs from server

import socket
import sys
import time
import threading

def printTimeAfterSync(currSimTime):
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    print(  "time after update is:\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )

def printTimeBeforeSync(currSimTime):
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    print(  "time before update is:\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )

# Sends a sync query to the server and calculates the simulated time based on the response
# Returns the new simulated time
def syncClocks():
    
    global sysTimeAfterSync, currSimTime

    # Update current simulated time since last sync
    currSimTime += (time.time() - sysTimeAfterSync) * (1 + drift)

    # Print time before syncing
    printTimeBeforeSync(currSimTime)

    # Store system time before sending sync request
    sysTimeBeforeSync = time.time()

    # Send sync request to server
    sock.sendto(b"sync_req", address)

    # Receive server time message
    data, addr = sock.recvfrom(1024)
    serverTime = float(data.decode() )   # Get server time from data

    # Calculate simulated round-trip time
    sysTimeAfterSync = time.time() # Update system time after sync
    realRoundTripTime = sysTimeAfterSync - sysTimeBeforeSync
    simRoundTripTime = realRoundTripTime * (1 + drift)
    
    # Update global simulated time with Cristian's algorithm
    currSimTime = serverTime + simRoundTripTime / 2

    # Print time after syncing
    printTimeAfterSync(currSimTime)


IP = "127.0.0.1"    # Server's IP
PORT = 2001 # Server's port

address = (IP, PORT)    # server address

skew = 2    # Difference between client's and server's clock times
drift = 10  # difference between ... clock frequencies

# Clock-sync query period
queryPeriod = skew / (2 * drift)

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )

sysTimeAfterSync = time.time()  # Initialize
currSimTime = time.time() + skew    # Initialize current simulated time with skew
printTimeAfterSync(currSimTime) # Initial output

# # Run the clock-sync on a separate thread every queryPeriod seconds
# while True:

# Spawn a thread to sync clock with server
threading.Thread(target = syncClocks).start()

# time.sleep(queryPeriod)   # Sleep to maintain query frequency/period