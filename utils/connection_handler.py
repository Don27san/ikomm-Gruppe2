import socket
from threading import Thread
from typing import Tuple
import queue
from utils import red


class ConnectionHandler:
    """
    ConnectionHandler provides a high-level interface for managing TCP connections, supporting both client and server modes. 
    It abstracts away the complexities of socket handling, message delimitation, and concurrent connection management.
    Features:
    - Can operate as a TCP client or server.
    - Handles incoming and outgoing data streams, ensuring messages are properly delimited and queued.
    - Uses a background thread to listen for new connections (server mode) and to process incoming messages.
    - Maintains an internal queue of received messages, each associated with the sender's address and socket.
    - Supports configurable timeout for message retrieval from the queue.
    - Provides methods to send messages and to close the underlying socket. 
    Args:
        timeout (int, optional): Timeout in seconds for retrieving messages from the internal queue. If None, waits indefinitely.
    Raises:
        Exception: On malformed message headers or connection errors during message extraction.
    Usage:
        handler = ConnectionHandler(timeout=5)
        handler.start_server('127.0.0.1', 8080)
        # or
        handler.start_client('127.0.0.1', 8080)
        ...
        msg, addr, sock = handler.recv_msg()
        handler.send_msg(b"response")
        handler.close()

    """      
    def __init__(self, timeout: int=None):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        self.msg_queue = queue.Queue()
        self.msg_queue_timeout = timeout

    def start_client(self, conn_ip, conn_port):
        self.socket.connect((conn_ip, conn_port))
        Thread(target=self._handle_new_connection, args=(self.socket, self.socket.getpeername()), daemon=True).start()
    

    def start_server(self, bind_ip : str, bind_port: int):
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((bind_ip, bind_port))
        self.socket.listen(5)
        Thread(target=self._server_listen, daemon=True).start()  # Start listener in background thread

    def _server_listen(self):
        while True:
            client_socket, addr = self.socket.accept()
            Thread(target=self._handle_new_connection, args=(client_socket, addr)).start()

    def _handle_new_connection(self, client_socket: socket.socket, addr: Tuple[str, int]):
        buffer = b''  # internal buffer for received data
        try:
            while True:
                try:
                    msg, buffer = self._extract_msg(client_socket, buffer)
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
  


    def _extract_msg(self, conn: socket.socket, buffer: bytes) -> Tuple[bytes, bytes]:
        """
        Retrieves data out of the raw buffer thus creating clear message boundaries from the stream.

        Returns:
            Tuple[bytes, bytes]: 
            - Single delimited message.
            - Superfluous data of the stream which we've already consumed during extraction of this message that needs to be preserved for the next message extraction.
        """
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


    def send_msg(self, data: bytes):
        self.socket.send(data)


    def recv_msg(self) -> Tuple[bytes, Tuple[str, int], socket.socket]:
        """
        Retrieves the next complete message in the internal message queue from any of the established connections.
        It returns information about the received message, the client's address, and provides the respective socket object for responding.

        Returns:
            Tuple[bytes, Tuple[str, int], socket.socket]: A 3-tuple in the following order:
                - msg (bytes): The full serialized message received.
                - addr (Tuple[str, int]): The client's address as a (host, port) tuple.
                - connection_socket (socket.socket): The socket object representing the client connection. Use this to send your respond to client of this exact connection. This is only relevant for the server to differentiate between connections. 
        """
        if self.msg_queue_timeout is not None:
            return self.msg_queue.get(timeout=self.msg_queue_timeout)
        else:
            return self.msg_queue.get()

    def close(self) -> None:
        try:
            self.socket.close()
        except Exception as e:
            red(f"{e}")