# UDP client that requests time synchs from server

import socket
import sys
import time
import threading

def printTimeAfterSync(currSimTime):
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    numSec = currSimTime % 60   # for more precision
    print(  "time after update is:\n" +
            "second: " + str(numSec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            , flush=True)

def printTimeBeforeSync(currSimTime):
    timeStruct = time.gmtime(currSimTime)   # Get UTC struct_time
    numSec = currSimTime % 60   # for more precision
    print(  "time before update is:\n" +
            "second: " + str(numSec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            , flush=True)

# Sends a sync query to the server and calculates the simulated time based on the response
# Returns the new simulated time
def syncClocks():

    global sysTimeAfterSync, currSimTime

    # Store system time before sending sync request
    sysTimeBeforeSync = time.time()

    # Send sync request to server
    sock.sendto(b"sync_req", serverAddress)

    # Receive server time message
    data, addr = sock.recvfrom(1024)
    serverTime = float(data.decode() )   # Get server time from data

    # Calculate simulated round-trip time
    sysTimeAfterSync = time.time() # Update system time after sync
    realRoundTripTime = sysTimeAfterSync - sysTimeBeforeSync

    # Update global simulated time with Cristian's algorithm
    currSimTime = serverTime + realRoundTripTime / 2

    # Print time after syncing
    printTimeAfterSync(currSimTime)

# Run one time-sync cycle
def runOneSyncCycle():
    
    # Spawn a thread to sync clock with server
    thread = threading.Thread(target = syncClocks, daemon = True)
    thread.start()

    # Sleep to maintain query frequency/period
    time.sleep(queryPeriod)

    # Check if thread has finished before continuing to next sync-cycle
    if thread.is_alive():
        print("Error: Query period is over but previous time packet has not been received. Exiting...")
        sys.exit()


if len(sys.argv) != 4:
    print("Expected 4 arguments. Exiting...", flush=True)
    sys.exit()

skew = int(sys.argv[1]) # Difference between client's and server's clock times
drift = float(sys.argv[2])  # difference between ... clock frequencies
PORT = int(sys.argv[3])  # Server's port

IP = "127.0.0.1"    # Server's IP
serverAddress = (IP, PORT)  # server address

# Clock-sync query period
queryPeriod = skew / (2 * abs(drift) )

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )

# Initialize current simulated time with skew
currSimTime = time.time() + skew

# Run initial sync cycle
runOneSyncCycle()

# Run the clock-sync on a separate thread every queryPeriod seconds
while True:

    # Update current simulated time since last sync
    currSimTime += (time.time() - sysTimeAfterSync) * (1 + drift)

    # Print time before syncing
    printTimeBeforeSync(currSimTime)

    # Run one sync cycle
    runOneSyncCycle()