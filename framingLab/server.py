#! /usr/bin/env python3

import os, re, socket, sys, time
from os.path import exists
from _thread import *
sys.path.append("../lib")
import params

def threaded_client(conn):
    # Will store attempted file that already existed or someone else is trying to write
    report_of_files = []
    
    # Create by array for file contents and info.
    file_data = bytearray([])

    while True:
        data = conn.recv(2048)
        file_data.extend(data)

        if not data:
            break

    file_data = file_data.decode()
    print('received data')
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
        print('file Name: ' + file_name)

        # Check file doesn't already exist by checking in the global list files names and in the directory
        global lock
        print('try to aquire lock')
        # lock.acquire() #aquire lock so that other threads don't check at the same time the existance of a file
        global list_of_names

        read = 0
        file_info_pointer += 1

        if file_name in list_of_names or exists('C:\\Users\\chris\\Downloads\\Python files\\Server DB\\' + file_name):
            report_of_files.append(file_data)
            # lock.release()
            continue #move on to the next file

        else:
            list_of_names.append(file_name)
            # lock.release()
        
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

    # Report to the client what files were not written 
    if len(report_of_files):
        report = "1 unable to send the following files: "
        for i in report_of_files:
            report += i + ", "

    else:
        report = '0 everything was send successfully'

    conn.sendall(report.encode())
    conn.close()
    conn.close()

ThreadCount = 0
list_of_names = []

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
    print('Connected by', addr)
    start_new_thread(threaded_client, (conn, ))
    ThreadCount += 1
