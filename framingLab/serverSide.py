#! /usr/bin/env python3

# Jonathan notes:
# server side should remain the same from the one provided, but the difference is, the server will echo back the whole thing that was send
# by the client so that the client can decompress the data and see if it got back what it just send. The server should then be expanded 
# to handle multiple requests by using forking calls. 

import os, re, socket, sys, time
sys.path.append("../lib")
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

# def save_file_server(socket, file_name, file_contents):

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

listenPort = paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

# Create socket, param 1: socket type for IPv4, param 2: socket type for protocol used to transport messages in the network
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# used to associate the socket with a specific network interface and port number(the physical components of PC used for networking)
# Think of the host as the person we want to talk to with email address listenAddr
s.bind((listenAddr, listenPort))

# enables a server to accept connections. Param is used to state the max. num of requests that can be queued.
s.listen(1)              # allow only one outstanding request

# Will store the names of the files that were received so that in the end we send their contents back
list_of_names = []

conn, addr = s.accept() # wait until incoming connection request (and accept it) and this socket is different from the listening one
if os.fork() == 0:      # child becomes server
    print('Connected by', addr)
    
    # Start receiving files
    while True:
        # first thing to receive is the length of the file name in bytes
        data = conn.recv(1024)
        
        if not data:
            # No more file contents
            break

        file_name_size = int(data.decode())

        # Next thing to receive is the actual file name
        data = conn.recv(1024)

        # Make sure that the name of the file is of the size that was given 
        file_name = data.decode()
        list_of_names.append(file_name)
        
        if(file_name_size != sys.getsizeof(file_name)):
            print("error, file name is not of specified size")
            continue

        
        # Next thing to receive is the size of the file
        data = conn.recv(1024)
        file_size = int(data.decode())

        # open a file with the send name and start writing the contents of it
        file = open(file_name,'w')

        # Next thing to receive is the contents of the file, for this we use a while loop to keep receiving until we no longer get data
        # use the size of the file to also know when to stop

        current_amount = 0

        while True:
            # Receive data of the file, write it to the file, and check whether we are done receiving data for that file
            data = (conn.recv(file_size)).decode()
            file.write(data)
            current_amount += sys.getsizeof(data)

            if(current_amount == file_size):
                file.close()
                break    # Move on to the next file
        

# We have exited all loops, will start sending the files back
if(len(list_of_names)):
    for current_file in list_of_names:
        # Send file name size
        data = str(sys.getsizeof(current_file)).encode()
        conn.sendall(data)

        # send the file name
        data = current_file.encode()
        conn.sendall(data)

        # Send file size 
        data = str(os.path.getsize(current_file)).encode()
        conn.sendall(data)

        # Send file contents
        file = open(current_file,'r')
        data = file.read().encode()
        conn.sendall(data)


conn.shutdown(socket.SHUT_WR)
