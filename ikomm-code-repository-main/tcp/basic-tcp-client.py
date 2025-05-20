# This script gives an overview over the structure of a basic TCP client and server
# It can't be run!

#
# Chat client
#
import socket
# Open socket (SOCK_STREAM for TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Connect socket to IP address and port
s.connect(("localhost", 9009))

while True:
    # Receive data
    data = s.recv(10000)

    if not data: break

    print(data)

#
# TCP Server
#
import socket
# Open socket (SOCK_STREAM for TCP)
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Bind socket to the localhost IP address and a certain port
s.bind(("0.0.0.0", 8090))
# Listen for one connection
s.listen(1)
# Accept incoming connection
conn, addr = s.accept()

while True:
    # Receive data
    data = conn.recv(1024)

    if not data:
        break

    print(data)
    # Send data back (echo)
    conn.sendall(data)

# Close connection
conn.close()
# Close socket
s.close()
