#! /usr/bin/env python3

# The client should send the compressed data and received back in order to decompress it(the data basically did a round trip) 
# in order to verify that we got everything back from the server that we send.

# V2 maybe add confirmation messages that are received from the server. 

import socket, sys, re, time, os
from textwrap import fill
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--delay'), 'delay', "0"),
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )


progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage  = paramMap["server"], paramMap["usage"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

s = None
for res in socket.getaddrinfo(serverHost, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
        print("creating sock: af=%d, type=%d, proto=%d" % (af, socktype, proto))
        s = socket.socket(af, socktype, proto)
    except socket.error as msg:
        print(" error: %s" % msg)
        s = None
        continue
    try:
        print(" attempting to connect to %s" % repr(sa))
        s.connect(sa)
    except socket.error as msg:
        print(" error: %s" % msg)
        s.close()
        s = None
        continue
    break

if s is None:
    print('could not open socket')
    sys.exit(1)

delay = float(paramMap['delay']) # delay before reading (default = 0s)
if delay != 0:
    print(f"sleeping for {delay}s")
    time.sleep(int(delay))
    print("done sleeping")

file_names = input('What files would you like transfer?\n').split(' ')

# Send the number of files first
number_of_files = '\\' + str(len(file_names)) + '\\'
s.send(number_of_files.encode())

# Client will send the size of the file name, the name of the file, the size of the file, and the contents of the file. 
# The file names will be specified in the command line
for i in file_names:
    file_data = []
    # Get file name
    file_name = i

    # Get file name size
    file_name_size = str(len(file_name))

    # Get the file size and contents
    file = open(file_name, 'r')
    data = file.read()
    file_size = str(len(data))
    
    file_data.append('\\')
    file_data.append(file_name_size)
    file_data.append('\\')
    file_data.append(file_name)
    file_data.append('\\')
    file_data.append(file_size)
    file_data.append('\\')
    file_data.append(data)
    file_data.append('\\')


    file_data = ''.join(file_data)

    # Finally send it
    s.send(file_data.encode())

# Wait for a report if any
report = bytearray([])

while True:
    # first thing on the byte array is the length of the file name in bytes
    data = s.recv(1024)

    # Add received data to byte array
    report.extend(data)

    if not data:
        # No more file contents
        break
    
report = report.decode()
print(report)

s.close()
