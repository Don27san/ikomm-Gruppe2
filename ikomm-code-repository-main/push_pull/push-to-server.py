import socket
import threading


def push_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    server_socket.settimeout(1)
    print("Push Server started and listening for connections.")

    client_socket, addr = server_socket.accept()
    print(f"Connected to client at {addr}")

    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"Server -> Received from client: {data.decode('ASCII')}")
        except socket.timeout:
            continue  # Check periodically
    server_socket.close()


def push_client(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    try:
        for i in range(10):  # Example: send data 10 times
            data = f"Message {i}, "
            print(f"Client -> Sent to server: {data}")
            sock.sendall(data.encode('ASCII'))
    finally:
        sock.close()


if __name__ == '__main__':
    # Start server
    server_thread = threading.Thread(target=push_server, args=('localhost', 9999))
    server_thread.daemon = True
    server_thread.start()

    # Start client
    client_thread = threading.Thread(target=push_client, args=('localhost', 9999))
    client_thread.daemon = True
    client_thread.start()

    client_thread.join()  # Wait for the client to finish
    print("\nClient has finished sending data.")
