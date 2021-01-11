# UDP time server that sends clients the server time

import socket
import sys
import time

IP = "127.0.0.1"    # Server's IP
PORT = 2001 # Server's port

def printConnected():
    timeStruct = time.gmtime(time.time() )
    print(  "Server connected to (\'" + str(IP) + "\', " + str(PORT) + ")\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )

delay = 1   # for simulating propagation delay

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )
sock.bind( (IP, PORT) )

while True:
    data, address = sock.recvfrom(1024) # Max. message size is 1024 bytes

    if data == b"sync_req":
        # Print information
        printConnected()
        
        time.sleep(delay)   # simulate client->server propagation delay
        currTime = time.time()  # time since epoch (unix time)
        time.sleep(delay)   # simulate server->client propagation delay
        printConnected()
        sock.sendto(str(currTime).encode(), address)    # send time to client