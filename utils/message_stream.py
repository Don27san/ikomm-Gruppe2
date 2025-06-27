import socket
from typing import Tuple

class MessageStream:
    """
    A TCP message stream handler for receiving structured messages over a socket connection 
    Parameters:
        connection_addr (str): The IP address to bind the server socket to.
        connection_port (int): The port number to bind the server socket to.
    Attributes:
        connection_socket (socket.socket): The server socket listening for incoming connections.
        conn (socket.socket): The accepted client connection socket.
        addr (tuple): The address of the connected client.
        buffer (bytes): Internal buffer for accumulating received data.
    Methods:
        recv_msg():
            Receives the next complete message from the stream.
            Reads data until a message with a valid header and payload is fully received.
            Returns:
                tuple: (msg, addr) where `msg` is the raw message bytes (including header and payload),
                       and `addr` is the address of the connected client.
                Returns None if the message is malformed or the connection is closed unexpectedly.
    """
    
    def __init__(self, connection_addr : str, connection_port : int):
        self.connection_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connection_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.connection_socket.bind((connection_addr, connection_port))
        self.connection_socket.listen(5)
        
        self.conn = None  # Current connection
        self.addr = None  # Current connection address
        self.buffer = b'' # Stores the data which we receive via TCP

    def recv_msg(self) -> Tuple[bytes, Tuple[str, int]]:
        """
        Receives a complete message from the connection, parsing the header and payload.
        The message format is expected to be: `b'<message_name>  <size>  <payload>\\n'`
        Reads from the connection until the full message (including header and payload) is available.
        Validates the message structure and ensures the message ends with a newline delimiter.
        Returns:
            Tuple[bytes, Tuple[str, int]]: A tuple containing the raw message bytes (including header and payload)
            and the address of the sender.
        Raises:
            Exception: If the header is malformed, the connection is closed prematurely, or the message does not end with a newline.
        """
        # Accept a new connection if we don't have one
        if self.conn is None:
            self.conn, self.addr = self.connection_socket.accept()

        # Reads until 2 spaces (header of message_name and payload length) are found
        while self.buffer.count(b' ') < 2:
            res = self.conn.recv(1024)
            if not res:
                raise Exception("Connection closed while reading header.")
            self.buffer += res

        # Retrieve message_name and payload length
        try:
            first_space_idx = self.buffer.index(b' ')
            second_space_idx = self.buffer.index(b' ', first_space_idx + 1)
            payload_length = int(self.buffer[first_space_idx + 1: second_space_idx].decode())
        except ValueError:
            raise Exception("Malformed header")
            

        payload_start_idx = second_space_idx + 1
        total_needed = payload_start_idx + payload_length + 1  # +1 for \n delimiter at the end of each message

        # Reads full payload
        while len(self.buffer) < total_needed:
            res = self.conn.recv(1024)
            if not res:
                raise Exception("Connection closed while reading payload.")
            self.buffer += res

        # Validates if message ends with newline
        if self.buffer[total_needed - 1] != ord('\n'):
            raise Exception("Expected newline delimiter after payload.")

        # Return message and clear its data from buffer to proceed in the queue
        msg = self.buffer[:total_needed]
        self.buffer = self.buffer[total_needed:]
        return msg, self.addr
    
    def close_connection(self):
        """
        Closes the current client connection while keeping the server socket open.
        """
        if self.conn:
            self.conn.close()
            self.conn = None
            self.addr = None
            self.buffer = b''  # Clear buffer when closing connection
    
    def close_server(self):
        """
        Closes the server socket and any current connection.
        """
        self.close_connection()
        if self.connection_socket:
            self.connection_socket.close()
    
    def reset_buffer(self):
        """
        Resets the internal buffer. Use this if you want to clear any partially received data.
        """
        self.buffer = b''