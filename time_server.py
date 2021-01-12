# UDP time server that sends clients the server time

import socket
import sys
import time
import threading

IP = "127.0.0.1"    # Server's IP
PORT = 2001 # Server's port

def printConnected(address):
    timeStruct = time.gmtime(time.time() )
    clientIP, clientPort = address
    print(  "Server connected to (\'" + str(clientIP) + "\', " + str(clientPort) + ")\n" +
            "second: " + str(timeStruct.tm_sec) + "\n" +
            "minute: " + str(timeStruct.tm_min) + "\n" +
            "hour: " + str(timeStruct.tm_hour) + "\n"
            )

# Sends server time to client
# Simulates propagation delay
def sendTimeToClient():
            
    time.sleep(delay)   # simulate client->server propagation delay
    serverTime = time.time()  # time since epoch (unix time)
    printConnected(address) # print connection info
    time.sleep(delay)   # simulate server->client propagation delay
    
    # send server time to client
    sock.sendto(str(serverTime).encode(), address)


delay = 1   # for simulating propagation delay

sock = socket.socket(   socket.AF_INET, # IP
                        socket.SOCK_DGRAM  # UDP
                        )
sock.bind( (IP, PORT) )

while True:
    data, address = sock.recvfrom(1024) # Max. message size is 1024 bytes

    if data == b"sync_req":
        # Spawn a new thread to handle the clock sync with client
        threading.Thread(target = sendTimeToClient, args = () ).start()