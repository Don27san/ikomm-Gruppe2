import socket


# Basic concept of an echo server using the TCP protocol
# Send messages back and forth between client and echo server
def tcp_server():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("0.0.0.0", 8090))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(data.decode("ASCII"))
                conn.sendall(data)


if __name__ == '__main__':
    tcp_server()
