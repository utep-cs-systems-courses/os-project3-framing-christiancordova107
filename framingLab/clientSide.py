#! /usr/bin/env python3

# The client should send the compressed data and received back in order to decompress it(the data basically did a round trip) 
# in order to verify that we got everything back from the server that we send.

import socket, sys, re, time, os
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
        print(" attempting to sect to %s" % repr(sa))
        s.sect(sa)
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


# Client will send the size of the file name, the name of the file, the size of the file, and the contents of the file. 
# The file names will be specified in the command line
for i in range(1, len(sys.argv) - 1):
    # Get file name 
    file_name = str(sys.argv[i])

    # Send file name size
    data = sys.getsizeof(file_name)
    s.sendall(data.encode())

    # Send file name
    data = file_name
    s.sendall(data.encode())

    file_size = os.path.getsize(file_name)

    # Send size of file
    data = file_size
    s.sendall(data.encode())

    # Send contents of file
    file = open(file_name, 'r')
    data = file.read()
    s.sendall(data.encode())



# At this point we will be receiving the files back(echo)
# Start receiving files
while True:
    # first thing to receive is the length of the file name in bytes
    data = s.recv(1024)

    if not data:
        # No more file contents
        break

    file_name_size = int(data.decode())

    # Next thing to receive is the actual file name
    data = s.recv(1024)

    # Make sure that the name of the file is of the size that was given 
    file_name = data.decode()
    
    if(file_name_size != sys.getsizeof(file_name)):
        print("error, file name is not of specified size")
        continue

    
    # Next thing to receive is the size of the file
    data = s.recv(1024)
    file_size = int(data.decode())

    # open a file with the send name and start writing the contents of it
    file = open(file_name,'w')

    # Next thing to receive is the contents of the file, for this we use a while loop to keep receiving until we no longer get data
    # use the size of the file to also know when to stop

    current_amount = 0

    while True:
        # Receive data of the file, write it to the file, and check whether we are done receiving data for that file
        data = (s.recv(file_size)).decode()
        file.write(data)
        current_amount += sys.getsizeof(data)

        if(current_amount == file_size):
            file.close()
            break    # Move on to the next file


print('done')
s.close()


# while True:
#     data = s.recv(1024).decode()
#     print("Received '%s'" % data)
#     if len(data) == 0:
#         break
# print("Zero length read.  Closing")
# s.close()
