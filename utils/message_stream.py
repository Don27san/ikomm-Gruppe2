import socket
from threading import Thread
from typing import Tuple
from utils import blue
import queue


class MessageStream:
    def __init__(self, connection_addr: str, connection_port: int):
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection_socket.bind((connection_addr, connection_port))
        self.connection_socket.listen(5)
        self.msg_queue = queue.Queue()
        Thread(target=self.listen, daemon=True).start()  # Start listener in background thread

    def listen(self):
        while True:
            client_socket, addr = self.connection_socket.accept()
            Thread(target=self.handle_new_client, args=(client_socket, addr)).start()

    def handle_new_client(self, client_socket: socket.socket, addr: Tuple[str, int]):
        buffer = b''
        try:
            while True:
                try:
                    msg, buffer = self.extract_msg(client_socket, buffer)
                    if msg:
                        self.msg_queue.put((msg, addr, client_socket))
                except (ConnectionResetError, BrokenPipeError) as e:
                    continue  # Retry — don't close
                except Exception as e:
                    print(f"Fatal error from {addr}: {e}. Closing connection.")
                    break  # Exit loop on fatal
        finally:
            client_socket.close()
            print(f"Closed connection with {addr}")
  

    def extract_msg(self, conn: socket.socket, buffer: bytes) -> Tuple[bytes, bytes]:
        # Read until 2 spaces are found: "name length payload\n"
        while buffer.count(b' ') < 2:
            res = conn.recv(1024)
            buffer += res

        # Parse header
        try:
            first_space = buffer.index(b' ')
            second_space = buffer.index(b' ', first_space + 1)
            payload_length = int(buffer[first_space + 1:second_space].decode())
        except ValueError:
            raise Exception("Malformed header")

        payload_start = second_space + 1
        total_needed = payload_start + payload_length + 1  # +1 for the \n

        while len(buffer) < total_needed:
            data = conn.recv(1024)
            if not data:
                raise Exception("Connection closed while reading payload.")
            buffer += data

        if buffer[total_needed - 1] != ord('\n'):
            raise Exception("Expected newline delimiter after payload.")

        msg = buffer[:total_needed]
        buffer = buffer[total_needed:]  # trim processed message
        return msg, buffer

    def recv_msg(self) -> Tuple[bytes, Tuple[str, int], socket.socket]:
        """
        Blocks until a complete message is available from any connected client.

        Returns:
            Tuple[bytes, Tuple[str, int], socket.socket]: A 3-tuple in the following order:
                - msg (bytes): The full raw message received (including header and payload).
                - addr (Tuple[str, int]): The client's address as a (host, port) tuple.
                - conn (socket.socket): The socket object representing the client connection.
        """
        return self.msg_queue.get()  # (msg, addr, conn)
