# Internet Communication Code Repository




## Concept

This repository provides a collection of Python scripts aimed at demonstrating various internet communication protocols and techniques such as TCP, UDP, DNS, HTTP, RTT measurement, congestion control, and push-pull communication architecture.
The goal is to demonstrate the implementation of the basic communication protocols

## File Overview
### 1. DNS
```
File: dns/dns-example.py
```
Example script for performing DNS lookups and handling DNS resolution.
Includes querying DNS servers and resolving domain names.
#### Run the DNS lookup:
```
python dns/dns-example.py
```
Enter the website address into the terminal (e.g. www.ce.cit.tum.de). Enter "quit" to end the lookup.
### 2. HTTP
```
Files:
    http/http-example-1.py
    http/http-example-2.py
    http_files/lkn-bild.jpg
```
HTTP example 1 sends out an HTTP request to the lkn server to fetch a text document. 
HTTP example 2 presents a local HTTP example and gives an overview over the structure of an HTTP request.
The lkn-bild.jpg is needed for the second example.
#### Run the HTTP scripts:
```
python http/<filename.py>
```
### 3. Push-Pull Communication
```
Files:
    push-to-server.py
    pull-from-server.py
```
#### Push-to-server.py:
Implements a push client that pushes data to a server. The server receives the data and prints it on receive in the terminal.
#### Pull-from-server.py:
Implements a pull client where clients request data, and the server responds with the latest data from the push server. The data is randomly generated.
#### Run the PUSH/PULL script:
```
python push_pull/<filename.py>
```
### 4. RTT Measurement
```
File: rtt-measurements.py
```
Measures round-trip time (RTT) to a local echo server.
Useful for network latency analysis.
The RTT measurements only vary when server and client are run on different machines.
#### Run the RTT script:
```
python rtt/rtt-measurements.py
```
### 5. TCP
```
Files:
    basic-tcp-client.py: Basic TCP client example.
    tcp-chat-client.py: Chat client that connects to a TCP server and exchanges messages.
    tcp-echo-server.py: TCP echo server that sends received messages back to the client.
```
#### basic-tcp-client.py:
This script gives an overview over the structure of a basic TCP client and server and how to set up a connection between them. It can't be run!
#### tcp-echo-server.py & tcp-chat-client.py:
First start the echo server and then the chat client. The chat client is able to send TCP messages to the echo server, which will be echoed back to the client and printed.
#### Run the TCP scripts:
```
python tcp/<filename.py>
```
### 6. UDP
```
Files:
    message_encoding.py
    udp_messenger.py
    udp-client.py
    udp-pinger.py
```
#### message_encoding.py
Demonstrates encoding and decoding messages using ASCII and UTF-8 over UDP.
#### udp-client.py:
This script gives an overview over the structure of a basic UDP client and server. It can't be run!
#### udp-messenger.py:
Basic UDP messenger that allows sending and receiving messages.

#### Run the UDP scripts:
```
python udp/<filename.py>
```
### 7. Client & Server
```
Files: 
    client.py
    server.py
```
Combines TCP, UDP, DNS, HTTP, and RTT functionalities into a single UI client. An additional basic project example is given to set a baseline.
The client can perform DNS lookups, RTT measurements, HTTP requests, and can send messages via TCP and UDP protocols.
The server has to be startet first for the client to connect to the server. The server manages connections for the PUSH and PULL requests, responds to HTTP requests, and echoes TCP/UDP messages.

#### Run the Server:
```
python server.py
```
#### Run the Client:
```
python client.py
```
#### Features
TCP and UDP Communication: Send and receive messages over TCP and UDP protocols.
Push-Pull Architecture: Demonstrates a push-pull communication model where data is pushed to clients or pulled from the server.
DNS Lookup: Perform DNS lookups and trace the route to DNS servers.
HTTP Requests: Make HTTP requests (GET/POST) to a server and handle responses.
RTT Measurement: Measure the round-trip time (RTT) between the client and server.
### 8. Requirements
```
File: requirements.txt
```
Contains the necessary Python libraries to run the project. 
#### Prerequisites:
```
Python 3.10+
```
Required libraries can be installed via requirements.txt:
```
pip install -r requirements.txt
``` 

## Authors and acknowledgment

## License
