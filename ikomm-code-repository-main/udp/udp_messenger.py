import socket
import threading
import time 


def udp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind(("0.0.0.0", 7073))  # "0.0.0.0" or "localhost" possible for sending locally
        print("UDP Server is running and waiting for data...")
        while True:
            data, addr = sock.recvfrom(1500)
            if not data:
                break
            print(f"Received from {addr}: {data.decode('utf-8')}")


def udp_client():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        dst = ("localhost", 7073)
        message = "Hello World!"
        print(f"UDP Client sending '{message}' to {dst}")
        sock.sendto(message.encode('utf-8'), dst)


# Running both UDP server and client in separate threads
server_thread = threading.Thread(target=udp_server, daemon=True)
client_thread = threading.Thread(target=udp_client)

server_thread.start()
time.sleep(0.1)  # Buffer to start the server
client_thread.start()
