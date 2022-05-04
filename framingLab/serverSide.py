#! /usr/bin/env python3

# Jonathan notes:
# server side should remain the same from the one provided, but the difference is, the server will echo back the whole thing that was send
# by the client so that the client can decompress the data and see if it got back what it just send. The server should then be expanded 
# to handle multiple requests by using forking calls. 

import os, re, socket, sys, time
from os.path import exists
from threading import Thread,Lock
import Threader
sys.path.append("../lib")
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

# Create socket, param 1: socket type for IPv4, param 2: socket type for protocol used to transport messages in the network
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.setblocking(0)

# used to associate the socket with a specific network interface and port number(the physical components of PC used for networking)
# Think of the host as the person we want to talk to with email address listenAddr
s.bind((listenAddr, listenPort))

# enables a server to accept connections. Param is used to state the max. num of requests that can be queued.
s.listen(1)              # allow only one outstanding request

# Will store the names of the files that were received so that in the end we send their contents back
# list_of_names = []

while True:
    conn, addr = s.accept() # wait until incoming connection request (and accept it) and this socket is different from the listening one
    Threader.Worker(conn, addr).start()
    # server = Thread(target=run,args=(conn, )) #Create thread that will handle the request