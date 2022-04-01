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
    
    # Create by array for file contents and info.
    file_data = bytearray([])

    # Start receiving files
    while True:
        # first thing on the byte array is the length of the file name in bytes
        data = conn.recv(1024)

        # Add received data to byte array
        file_data.extend(data)

        if not data:
            # No more file contents
            break

    file_data = file_data.decode()
    
    # Pointer that will point to how much to read and counter of how much we have read
    file_info_pointer = 1
    read = 0
    non_excess = ''
    excess = ''
    file_name_size = ''
    file_name = ''
    file_size = ''
    file_contents = ''
    number_of_files = ''

    while (file_data[file_info_pointer] != '\\'):
        number_of_files += file_data[file_info_pointer]
        file_info_pointer += 1

    file_info_pointer += 1
    number_of_files = int(number_of_files)
        
    for i in range(number_of_files):
        while (file_data[file_info_pointer] != '\\'):
            file_name_size += file_data[file_info_pointer]
            file_info_pointer += 1
            
        file_name_size = int(file_name_size)
        file_info_pointer += 1

        while (file_data[file_info_pointer] != '\\' and read <=file_name_size) :
            file_name += file_data[file_info_pointer]
            file_info_pointer += 1
            read += 1

        read = 0
        file_info_pointer += 1

        while (file_data[file_info_pointer] != '\\'):
            file_size += file_data[file_info_pointer]
            file_info_pointer += 1
        
        file_size = int(file_size)
        file_info_pointer += 1

        while (file_data[file_info_pointer] != '\\' and read <=file_size) :
            file_contents += file_data[file_info_pointer]
            file_info_pointer += 1
            read += 1

        file_info_pointer += 1

        file = open('C:\\Users\\chris\\Downloads\\Python files\\Server DB\\' + file_name, 'w')
        file.write(file_contents)
        file.close()
            
        print('file name: ' + file_name + '\n' + file_contents)
                

    # Start decomposing files
    # while True:
    #     if(len(excess)):
    #         file_name_size = int(excess[0].decode())
    #         file_name = excess[1 :].decode()
    #     non_excess = ''
    #     excess = ''

    #     print('file pointer: ' + str(file_info_pointer))
    #     file_name_size = file_data[file_info_pointer]
    #     file_info_pointer += 1
    #     file_name = ''
    #     print('file name size: ' + str(file_name_size))

    #     while read <= file_name_size:
    #         data = (file_data[file_info_pointer]).decode()
    #         file_info_pointer += 1 
            
    #         non_excess = ''
    #         size_of_data = sys.getsizeof(data)

    #         if(size_of_data + read > file_name_size):
    #             difference = file_name_size - size_of_data + read
    #             non_excess = data[ : size_of_data - difference]
    #             excess = data[size_of_data - difference :]
    #             file_name += non_excess
    #             break

    #         else:
    #             print(data)
    #             file_name += data
    #             read += size_of_data

    #     print(file_name)
            
    #     # This can contain the size of the file
    #     if(excess):
    #         file_size = excess[0].decode()
    #         excess = excess[1:].decode()
    #     else:
    #         file_size = file_data[file_info_pointer]

    #     print('the file size is: ' + str(file_size))

    #     file_contents = excess 
    #     read = 0

    #     while read <= file_size: 
    #         data = file_data[file_info_pointer]
    #         file_info_pointer += 1 
            
    #         non_excess = ''
    #         size_of_data = sys.getsizeof(data)

    #         if(size_of_data + read > file_name_size):
    #             difference = file_size - size_of_data + read
    #             non_excess = (data)[ : size_of_data - difference]
    #             excess = (data)[size_of_data - difference :]
    #             file_contents += non_excess.decode()
    #             break

    #         else:
    #             file_contents += data.decode()
    #             read += size_of_data

    #     file = open(file_name, 'w')
    #     file.write(file_contents.decode())
    #     file.write('v2')
    #     file.close()

conn.close()
# conn.shutdown(socket.SHUT_WR)
