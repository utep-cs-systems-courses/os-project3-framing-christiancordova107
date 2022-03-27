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
        
    print(file_data[0])
    print(file_data[1])
    print(file_data[2])
    
    # Pointer that will point to how much to read and counter of how much we have read
    file_info_pointer = 0
    read = 0
    non_excess = ''
    excess = ''
    file_name_size = ''
    file_name = ''

    # Start decomposing files
    while True:
        if(len(excess)):
            print('hello')
            file_name_size = int(excess[0].decode())
            file_name = excess[1 :].decode()
        non_excess = ''
        excess = ''

        print('file pointer: ' + str(file_info_pointer))
        file_name_size = file_data[file_info_pointer]
        file_info_pointer += 1
        file_name = ''
        print('file name size: ' + str(file_name_size))

        while read <= file_name_size:
            data = (file_data[file_info_pointer]).decode()
            file_info_pointer += 1 
            
            non_excess = ''
            size_of_data = sys.getsizeof(data)

            if(size_of_data + read > file_name_size):
                difference = file_name_size - size_of_data + read
                non_excess = data[ : size_of_data - difference]
                excess = data[size_of_data - difference :]
                file_name += non_excess
                break

            else:
                print(data)
                file_name += data
                read += size_of_data

        print(file_name)
            
        # This can contain the size of the file
        if(excess):
            file_size = excess[0].decode()
            excess = excess[1:].decode()
        else:
            file_size = file_data[file_info_pointer]

        print('the file size is: ' + str(file_size))

        file_contents = excess 
        read = 0

        while read <= file_size: 
            data = file_data[file_info_pointer]
            file_info_pointer += 1 
            
            non_excess = ''
            size_of_data = sys.getsizeof(data)

            if(size_of_data + read > file_name_size):
                difference = file_size - size_of_data + read
                non_excess = (data)[ : size_of_data - difference]
                excess = (data)[size_of_data - difference :]
                file_contents += non_excess.decode()
                break

            else:
                file_contents += data.decode()
                read += size_of_data
        # # Read from current position to currentPosition + fileSize to get the file name
        # file_name = file_data[file_info_pointer : file_name_size + file_info_pointer].decode()
        # file_info_pointer += file_name_size + 1
        # print('The file name is: ' + file_name)

        # file_size = file_data[file_info_pointer]
        # file_info_pointer += 1
        # print('the file size is: ' + str(file_size))

        # Read from current position to currentPosition + fileSize to get the file contents
        # file_contents = file_data[file_info_pointer : file_size + file_info_pointer]
        # file_info_pointer += file_name_size + 1
        # print('file contents: ' + file_contents.decode())

        file = open(file_name, 'w')
        file.write(file_contents.decode())
        file.write('v2')
        file.close()

        # pointer should be pointing to the next file, if there's more files to read
        

        # open a file with the send name and start writing the contents of it
#         file = open(file_name,'w')

#         # Next thing to receive is the contents of the file, for this we use a while loop to keep receiving until we no longer get data
#         # use the size of the file to also know when to stop

#         current_amount = 0

#         while True:
#             # Receive data of the file, write it to the file, and check whether we are done receiving data for that file
#             data = (conn.recv(file_size)).decode()
#             file.write(data)
#             current_amount += sys.getsizeof(data)

#             if(current_amount == file_size):
#                 file.close()
#                 break    # Move on to the next file
        

# # We have exited all loops, will start sending the files back
# if(len(list_of_names)):
#     for current_file in list_of_names:
#         # Send file name size
#         data = str(sys.getsizeof(current_file)).encode()
#         conn.send(data)

#         # send the file name
#         data = current_file.encode()
#         conn.send(data)

#         # Send file size 
#         data = str(os.path.getsize(current_file)).encode()
#         conn.send(data)

#         # Send file contents
#         file = open(current_file,'r')
#         data = file.read().encode()
#         conn.send(data)


conn.shutdown(socket.SHUT_WR)
