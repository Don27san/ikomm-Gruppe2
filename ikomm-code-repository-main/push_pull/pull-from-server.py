# TODO: GET anfrage nach dateien
import socket
import threading
import time
import random


def pull_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Pull Server started and listening for connections.")
    
    client_socket, addr = server_socket.accept()
    print(f"Connected to {addr}")
    
    server_socket.settimeout(1)  # Set timeout

    while True:
        try:
            data = client_socket.recv(16)
            # Check if data is "GET Data"
            if data.decode("ASCII") == "GET Data":
                for _ in range(0, 100):
                    # Simulate data generation
                    data = f"Data: {random.random()}\n"
                    client_socket.sendall(data.encode("ASCII"))
        except socket.timeout:
            print(socket.timeout)
            continue  # Check periodically
        break
    client_socket.close()


def pull_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    sock.settimeout(1)  # Set timeout

    print("Pull Client started and connected to server.")
    sock.sendall("GET Data".encode("ASCII"))
    
    # Receive data
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            print("Received:\n", data.decode("ASCII"))
        except socket.timeout:
            continue  # Check periodically
    sock.close()


if __name__ == '__main__':
    # Start server
    server_thread = threading.Thread(target=pull_server, args=('localhost', 9999), daemon=True)
    server_thread.start()

    # Give the server a second to start up
    time.sleep(3)

    # Start client
    client_thread = threading.Thread(target=pull_client, args=('localhost', 9999), daemon=True)
    client_thread.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Keyboard interrupt, exiting.")
    client_thread.join()  # Wait for the client to finish
    server_thread.join()

    