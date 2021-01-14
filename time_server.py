# UDP time server that sends clients the server time

import socket
import sys
import time
import threading
import os

def printTime():
    timeStruct = time.gmtime(time.time() )  # convert to time_struct
    numSec = time.time() % 60   # for more precision
    print(  "second: " + str(numSec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            , flush=True)

def printConnected(address):
    IP, port = address
    print("Server connected to (\'" + str(IP) + "\', " + str(port) + ")", flush=True)
    printTime()

# Sends server time to client
# Simulates propagation delay
def sendTimeToClient(clientAddress):
            
    time.sleep(delay)   # simulate client->server propagation delay
    serverTime = time.time()    # time since epoch (unix time)
    printConnected(clientAddress) # print connection info
    time.sleep(delay)   # simulate server->client propagation delay
    
    # send server time to client
    sock.sendto(str(serverTime).encode(), clientAddress)

# Starts interactive mode to handle user input
def interactiveUserInput():
    while True:
        # Valid commands are:
        #   time: print current time
        #   exit: exit program
        cmd = input()

        if cmd == "time":
            printTime()

        elif cmd == "exit":
            print("Exiting...", flush=True)
            os.kill(os.getpid(), 1) # Kill whole process

if len(sys.argv) != 3:
    print("Expected 3 arguments. Exiting...", flush=True)
    sys.exit()

delay = float(sys.argv[1]) # for simulating propagation delay
PORT = int(sys.argv[2])  # Server port

IP = "127.0.0.1"    # Server's IP

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )
sock.bind( (IP, PORT) )

# Spawn a new thread to handle user input
threading.Thread(target=interactiveUserInput, args=() ).start()

while True:
    data, clientAddress = sock.recvfrom(1024) # Max. message size is 1024 bytes

    if data == b"sync_req":
        # Spawn a new thread to handle the clock sync with client
        threading.Thread(target = sendTimeToClient, args = (clientAddress,) ).start()