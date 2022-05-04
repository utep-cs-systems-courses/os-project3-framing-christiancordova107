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

# # Create lock
# lock = Lock()

# def run(socket):
#     # Will store attempted file that already existed or someone else is trying to write
#     report_of_files = []

#     print('Connected by', addr)
    
#     # Create by array for file contents and info.
#     file_data = bytearray([])

#     # Start receiving files
#     while True:
#         # first thing on the byte array is the length of the file name in bytes
#         data = conn.recv(1024)

#         # Add received data to byte array
#         file_data.extend(data)

#         if not data:
#             # No more file contents
#             break

#     file_data = file_data.decode()
    
#     # Pointer that will point to how much to read and counter of how much we have read
#     file_info_pointer = 1
#     read = 0
#     non_excess = ''
#     excess = ''
#     file_name_size = ''
#     file_name = ''
#     file_size = ''
#     file_contents = ''
#     number_of_files = ''

#     while (file_data[file_info_pointer] != '\\'):
#         number_of_files += file_data[file_info_pointer]
#         file_info_pointer += 1

#     file_info_pointer += 1
#     number_of_files = int(number_of_files)
        
#     for i in range(number_of_files):
#         while (file_data[file_info_pointer] != '\\'):
#             file_name_size += file_data[file_info_pointer]
#             file_info_pointer += 1
            
#         file_name_size = int(file_name_size)
#         file_info_pointer += 1

#         while (file_data[file_info_pointer] != '\\' and read <=file_name_size) :
#             file_name += file_data[file_info_pointer]
#             file_info_pointer += 1
#             read += 1

#         # Check file doesn't already exist by checking in the global list files names and in the directory
#         lock.acquire() #aquire lock so that other threads don't check at the same time the existance of a file
#         global list_of_names

#         read = 0
#         file_info_pointer += 1

#         if file_name in list_of_names or exists('C:\\Users\\chris\\Downloads\\Python files\\Server DB\\' + file_name):
#             report_of_files.append(file_data)
#             lock.release()
#             continue #move on to the next file

#         else:
#             list_of_names.append(file_name)
#             lock.release()
        
#         while (file_data[file_info_pointer] != '\\'):
#             file_size += file_data[file_info_pointer]
#             file_info_pointer += 1
        
#         file_size = int(file_size)
#         file_info_pointer += 1

#         while (file_data[file_info_pointer] != '\\' and read <=file_size) :
#             file_contents += file_data[file_info_pointer]
#             file_info_pointer += 1
#             read += 1

#         file_info_pointer += 1

#         file = open('C:\\Users\\chris\\Downloads\\Python files\\Server DB\\' + file_name, 'w')
#         file.write(file_contents)
#         file.close()
            
#         print('file name: ' + file_name + '\n' + file_contents)

#     # Report to the client what files were not written 
#     if len(report_of_files):
#         report = "1 unable to send the following files: "
#         for i in report_of_files:
#             report += i + ", "

#     else:
#         report = '0 everything was send successfully'

#     socket.sendall(report.encode())
#     conn.close()    



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
    







# if os.fork() == 0:      # child becomes server
#     print('Connected by', addr)
    
#     # Create by array for file contents and info.
#     file_data = bytearray([])

#     # Start receiving files
#     while True:
#         # first thing on the byte array is the length of the file name in bytes
#         data = conn.recv(1024)

#         # Add received data to byte array
#         file_data.extend(data)

#         if not data:
#             # No more file contents
#             break

#     file_data = file_data.decode()
    
#     # Pointer that will point to how much to read and counter of how much we have read
#     file_info_pointer = 1
#     read = 0
#     non_excess = ''
#     excess = ''
#     file_name_size = ''
#     file_name = ''
#     file_size = ''
#     file_contents = ''
#     number_of_files = ''

#     while (file_data[file_info_pointer] != '\\'):
#         number_of_files += file_data[file_info_pointer]
#         file_info_pointer += 1

#     file_info_pointer += 1
#     number_of_files = int(number_of_files)
        
#     for i in range(number_of_files):
#         while (file_data[file_info_pointer] != '\\'):
#             file_name_size += file_data[file_info_pointer]
#             file_info_pointer += 1
            
#         file_name_size = int(file_name_size)
#         file_info_pointer += 1

#         while (file_data[file_info_pointer] != '\\' and read <=file_name_size) :
#             file_name += file_data[file_info_pointer]
#             file_info_pointer += 1
#             read += 1

#         read = 0
#         file_info_pointer += 1

#         while (file_data[file_info_pointer] != '\\'):
#             file_size += file_data[file_info_pointer]
#             file_info_pointer += 1
        
#         file_size = int(file_size)
#         file_info_pointer += 1

#         while (file_data[file_info_pointer] != '\\' and read <=file_size) :
#             file_contents += file_data[file_info_pointer]
#             file_info_pointer += 1
#             read += 1

#         file_info_pointer += 1

#         file = open('C:\\Users\\chris\\Downloads\\Python files\\Server DB\\' + file_name, 'w')
#         file.write(file_contents)
#         file.close()
            
#         print('file name: ' + file_name + '\n' + file_contents)


# conn.close()
# conn.shutdown(socket.SHUT_WR)
