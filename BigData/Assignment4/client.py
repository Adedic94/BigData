#!/usr/bin/env python

import socket

# the client must specify an address to connect to. 
# Here, we're connecting to the server on the same machine
SERVER_ADDRESS = ''
SERVER_PORT = 22222

# Create the socket
c = socket.socket()

# Connect to the server. 
c.connect((SERVER_ADDRESS, SERVER_PORT))

try:
    input = raw_input
except NameError:
    pass

print("Connected to " + str((SERVER_ADDRESS, SERVER_PORT)))
while True:
    try:
        data = input("Enter some data: ")
    except EOFError:
        print("\nOkay. Leaving. Bye")
        break

    if not data:
        print("Can't send empty string!")
        print("Ctrl-D [or Ctrl-Z on Windows] to exit")
        continue

    data = data.encode()

    # Send data to server
    c.send(data)

    # Receive response from server
    data = c.recv(2048)
    if not data:
        print("Server abended. Exiting")
        break

    data = data.decode()

    print("Got this string from server:")
    print(data + '\n')

c.close()