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

file_names = input('What files would you like transfer? Please separate the nammes by using a comma\n').split(' ')

# Create the bytearray that will keep the info. of the file and will be send all at once.
# file_data = bytearray()
file_data = []

# Client will send the size of the file name, the name of the file, the size of the file, and the contents of the file. 
# The file names will be specified in the command line
for i in file_names:
    # Create the bytearray that will keep the info. of the file and will be send all at once.

    # Get file name 
    file_name = i

    # Get file name size
    file_name_size = str(len(file_name))

    # Get the file size and contents
    file = open(file_name, 'r')
    data = file.read()
    file_size = str(len(data))
    
    file_data.append(file_name_size)
    file_data.append(file_name)
    file_data.append(file_size)
    file_data.append(data)


    file_data = ''.join(file_data)
    # # append the file name
    # data = file_name
    # file_data.extend(data.encode())

    # # Get the file size and the contents
    # file = open(file_name, 'r')
    # data = file.read()
    # file_size = len(data)

    # # Append size of file
    # file_data.append(file_size)

    # # Append contents of file
    # file_data.extend(data.encode())

    # Finally send it 
    print(file_data)
    s.sendall(file_data.encode())



# At this point we will be receiving the files back(echo)
# Start receiving files
# while True:
#     # Receiving all the info of the file and the contents
#     data = s.recv(1024)

#     if not data:
#         # No more file contents
#         break

#     print(data.decode())
#     file = open(file_name,'w')

#     # Next thing to receive is the contents of the file, for this we use a while loop to keep receiving until we no longer get data
#     # use the size of the file to also know when to stop

#     current_amount = 0

#     # write to the file
#     file.write(data)
#     current_amount += sys.getsizeof(data)

#     if(current_amount == file_size):
#         file.close()
#         break    # Move on to the next file


# print('done')
s.close()
