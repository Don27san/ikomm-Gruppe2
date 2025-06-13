# This script gives an overview over the structure of a basic UDP client and server
# It can't be run!


# ASCII Introduction

text = "Lehrstuhl für Kommunikationsnetze"
type(text)
try:
    data = text.encode('ASCII')  # <- ERROR
except Exception as e:
    print(e)
finally:
    pass

data = text.encode('UTF-8')
type(data)

data.decode('ASCII')  # <- ERROR
data.decode('UTF-8')


##
# UDP Server
##
# Console

# EMPFÄNGER:

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

sock.bind(("0.0.0.0", 7073))

data, addr = sock.recvfrom(1500)

# CONSOLE
# SENDER:

import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

dst = ("ik.lkn.ei.tum.de", 7073)

sock.sendto(b'Hello World!', dst)

