#!/usr/bin/env python

import socket

# Optionally set a specific address. This (the empty string) will listen on all
# the local machine's IPv4 addresses. 
SERVER_ADDRESS = ''

# Set a specific port number
SERVER_PORT = 22222

# Create the socket
s = socket.socket()

# Optional: this allows the program to be immediately restarted after exit.
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Bind to the desired address(es) and port.
s.bind((SERVER_ADDRESS, SERVER_PORT))

s.listen(5)

print("Listening on address %s. Kill server with Ctrl-C" %
      str((SERVER_ADDRESS, SERVER_PORT)))

# Now we have a listening endpoint from which we can accept incoming
# connections. 
while True:
    c, addr = s.accept()
    print("\nConnection received from %s" % str(addr))

    while True:
        data = c.recv(2048)
        if not data:
            print("End of file from client. Resetting")
            break

        data = data.decode()

        print("Received '%s' from client" % data)

        data = "Hello, " + str(addr) + ". I got this from you: '" + data + "'"
        data = data.encode()

        # Send the modified data back to the client.
        c.send(data)

    c.close()