import socket
import threading
import random


data_storage = {
    "Temperature": [],
    "Humidity": [],
    "Pressure": []
}


class DataServer:
    """Class to handle data transmission server for push and pull methods."""

    @staticmethod
    def handle_client_connection(conn):
        """
        Handle client connection for both push and pull data transmission.

        :param conn: The connection object for the client.
        """
        try:
            while True:
                request = conn.recv(1024).decode('utf-8')
                if not request:
                    break
                if "GET DATA" in request:
                    response = ",".join([f"{data_type}:{random.uniform(0, 100)}" for data_type in data_storage])
                    conn.sendall(response.encode('utf-8'))
                else:
                    data_pairs = request.split(',')
                    for data_pair in data_pairs:
                        data_type, value = data_pair.split(':')
                        data_storage[data_type].append(float(value))
                    conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        except Exception as e:
            print(f"Push/Pull - Connection error: {e}")
        finally:
            conn.close()

    @staticmethod
    def start_push_server():
        """Start the push server to accept data from clients."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', 8001))
            server_socket.listen(5)
            print('Push server - Running on port 8001...')
            while True:
                conn, addr = server_socket.accept()
                print(f"Push server - Connected by {addr}")
                DataServer.handle_push_connection(conn, addr)

    @staticmethod
    def handle_push_connection(conn, addr):
        """
        Handle the connection for the push server.

        :param conn: The connection object for the client.
        :param addr: The address of the client.
        """
        try:
            while True:
                request = conn.recv(1024).decode('utf-8')
                if not request:
                    break
                data_pairs = request.split(',')
                for data_pair in data_pairs:
                    data_type, value = data_pair.split(": ")
                    data_storage[data_type].append(float(value))
                conn.sendall(b"HTTP/1.1 200 OK\r\n\r\n")
        except Exception as e:
            print(f"Push server - Error: {e}")
        finally:
            conn.close()
            print(f"Push server - Connection with {addr} closed")

    @staticmethod
    def start_pull_server():
        """Start the pull server to send data to clients."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as pull_socket:
            pull_socket.bind(('localhost', 8002))
            pull_socket.listen(5)
            print('Pull server - Running on port 8002...')
            while True:
                conn, addr = pull_socket.accept()
                threading.Thread(target=DataServer.handle_pull_connection, args=(conn, addr)).start()

    @staticmethod
    def handle_pull_connection(conn, addr):
        """
        Handle the connection for the pull server.

        :param conn: The connection object for the client.
        :param addr: The address of the client.
        """
        print(f"Pull server - Connected by {addr}")
        try:
            while True:
                request = conn.recv(1024).decode('utf-8')
                if not request:
                    break
                if "GET DATA" in request:
                    response = ",".join(
                        [f"{data_type}:{data_storage[data_type][-1]}" if data_storage[data_type] else f"{data_type}:N/A"
                         for data_type in data_storage])
                    conn.sendall(response.encode('utf-8'))
                else:
                    conn.sendall(b"HTTP/1.1 400 Bad Request\r\n\r\n")
        except Exception as e:
            print(f"Pull server - Error: {e}")
        finally:
            print(f"Pull server - Connection with {addr} closed")
            conn.close()


class UDPServer:
    """Class to handle the UDP echo server."""

    @staticmethod
    def start_server():
        """Start the UDP echo server."""
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
            sock.bind(("0.0.0.0", 7073))
            print("UDP Server - Running and waiting for data...")
            while True:
                data, addr = sock.recvfrom(1024)
                print(f"UDP - Received from {addr}: {data.decode('utf-8')}")
                sock.sendto(data, addr)


class TCPServer:
    """Class to handle the TCP echo server."""

    @staticmethod
    def start_server():
        """Start the TCP echo server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind(("0.0.0.0", 8090))
            sock.listen()
            print("TCP Server - Running and waiting for connections...")
            while True:
                conn, addr = sock.accept()
                threading.Thread(target=TCPServer.handle_client, args=(conn, addr)).start()

    @staticmethod
    def handle_client(conn, addr):
        """
        Handle a client connection for the TCP echo server.

        :param conn: The connection object for the client.
        :param addr: The address of the client.
        """
        print(f"TCP - Connected by {addr}")
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                print(f"TCP - Received: {data.decode('utf-8')}")
                conn.sendall(data)
        print(f"TCP - Connection with {addr} closed")


class HTTPServer:
    """Class to handle the HTTP server."""

    @staticmethod
    def handle_request(conn):
        """
        Handle an HTTP request from a client.

        :param conn: The connection object for the client.
        """
        request = conn.recv(1024).decode('utf-8')
        headers = request.split('\n')
        filename = headers[0].split()[1]
        if filename == '/':
            filename = '/index.html'
        try:
            with open(filename, 'rb') as f:
                response = f.read()
                print(f"HTTP - GET Request for {filename}")
            conn.sendall(b'HTTP/1.1 200 OK\r\n\r\n' + response)
        except FileNotFoundError:
            conn.sendall(b'HTTP/1.1 404 NOT FOUND\r\n\r\nFile Not Found')

    @staticmethod
    def start_server():
        """Start the HTTP server."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind(('localhost', 8080))
            server_socket.listen(5)
            print('HTTP Server - Running on port 8080...')
            while True:
                conn, addr = server_socket.accept()
                HTTPServer.handle_request(conn)
                conn.close()


if __name__ == "__main__":
    # Start all servers in separate threads
    threading.Thread(target=UDPServer.start_server).start()
    threading.Thread(target=TCPServer.start_server).start()
    threading.Thread(target=HTTPServer.start_server).start()
    threading.Thread(target=DataServer.start_push_server).start()
    threading.Thread(target=DataServer.start_pull_server).start()
