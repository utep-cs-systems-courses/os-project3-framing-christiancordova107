#! /usr/bin/env python3

import sys,os
import socket
import threading
from threading import Thread
from time import time
from os.path import exists

list_of_names = []
threadNum = 0
lock = threading.Lock()

class Worker(Thread):
    def __init__(self, conn, addr):
        global threadNum
        Thread.__init__(self, name="Thread-%d" % threadNum)
        threadNum += 1
        self.conn = conn
        self.addr = addr

    def run(self):
        # Will store attempted file that already existed or someone else is trying to write
        report_of_files = []

        print('Connected by', self.addr)
        
        number_of_files = bytearray([])
        
        # Get the number of files
        while True:
            data = self.conn.recv(1024)
            number_of_files.extend(data)

            temp = number_of_files.decode()

            if not data or temp.count('\\') == 2:
                break
        
        file_info_pointer = 1
        number_of_files = number_of_files.decode()

        temp = ''

        while(number_of_files[file_info_pointer] != '\\'):
            temp += number_of_files[file_info_pointer]
            file_info_pointer += 1

        number_of_files = int(temp)

        for i in range(number_of_files):
            read = 0
            file_info_pointer = 1
            expected = 5
            file_name_size = ''
            file_name = ''
            file_size = ''
            file_contents = ''
            file_data = bytearray([])

            # Start receiving files
            while True:
                data = self.conn.recv(1024)
                # Add received data to byte array
                file_data.extend(data)

                temp = file_data.decode()

                if(temp.count('\\') == 5): #we have the size info
                    file_data = file_data.decode()

                    # Get the file name size
                    while (file_data[file_info_pointer] != '\\'):
                        file_name_size += file_data[file_info_pointer]
                        file_info_pointer += 1
                    
                    expected += len(file_name_size)
                    file_name_size = int(file_name_size)
                    expected += file_name_size
                    file_info_pointer += 1

                    # Get the file name
                    while (file_data[file_info_pointer] != '\\') :
                        file_name += file_data[file_info_pointer]
                        file_info_pointer += 1

                    # Check file doesn't already exist by checking in the global list files names and in the directory
                    global lock
                    lock.acquire() #aquire lock so that other threads don't check at the same time the existance of a file
                    write_flag = False
                    global list_of_names
                    file_info_pointer += 1

                    if file_name in list_of_names or exists('/home/christiancor10/project2/os-project3-framing-christiancordova107/framingLab/DBServer/' + file_name):
                        report_of_files.append(file_name)
                        lock.release()

                    else:
                        list_of_names.append(file_name)
                        lock.release()
                        write_flag = True

                    # Get the file size
                    while (file_data[file_info_pointer] != '\\'):
                        file_size += file_data[file_info_pointer]
                        file_info_pointer += 1
                
                    expected += len(file_size)
                    file_size = int(file_size)
                    expected += file_size
                    file_info_pointer += 1

                    # get the file contents
                    while (file_data[file_info_pointer] != '\\'): # and read <=file_size) :
                        file_contents += file_data[file_info_pointer]
                        file_info_pointer += 1
                        read += 1

                    file_info_pointer += 1

                    if(write_flag):
                        file = open('/home/christiancor10/project2/os-project3-framing-christiancordova107/framingLab/DBServer/' + file_name, 'w')
                        file.write(file_contents)
                        file.close()

                    if not data or expected == len(file_data):
                        break

        # Report to the client what files were not written 
        if len(report_of_files):
            report = "1 unable to send the following files: "
            for i in report_of_files:
                report += i + ", "

        else:
            report = '0 everything was send successfully'

        self.conn.sendall(report.encode())
        self.conn.close()
        print('done')