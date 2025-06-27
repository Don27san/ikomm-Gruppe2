import socket
from utils import blue, green, red, yellow, serialize_msg, parse_msg, connect_client

import socket
import threading
from typing import Callable

# Steps Server:
# MessageStream that threads new connections with _handle_client to receive and send data per client
# _handle_client gets handle_client function from location service in handle_connections to know what to do with all sorts of message
# Only open new thread if connection to that client not yet established
# Missing Messages: send and handle incoming PINGs, HANGUP,
# Acks und Resend handled implicitly

# Todos:
# Handling of multiple clients on server side
# Sending and receiving Ping, Hangup, correct Server UDP port and unsupported Message on Server and Client side (evtl. eigene Klasse)
# replace thread with asyncio
# try catch exception in all my programs


class MessageStream:
    """
    A threaded TCP server that accepts multiple client connections and handles each
    in a dedicated thread. Each message is parsed according to the format:
        <message_name> <payload_size> <payload>\n
    """

    def __init__(self, host: str, port: int, handler: Callable[[bytes, tuple, socket.socket], None]):
        """
        Initializes the TCP server.

        Args:
            host (str): Host/IP to bind.
            port (int): Port to listen on.
            handler (Callable): Function to call for each complete message.
                                It receives (message_bytes, client_address, client_socket).
        """
        self.host = host
        self.port = port
        self.handler = handler
        self.running = True

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        """
        Starts the TCP server loop that accepts new clients.
        Each client is handled in a separate thread.
        """
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen(5)
        print(f"[MessageStream] Listening on {self.host}:{self.port}")

        while self.running:
            try:
                conn, addr = self.server_socket.accept()
                print(f"[MessageStream] Accepted connection from {addr}")
                threading.Thread(target=self._handle_client, args=(conn, addr), daemon=True).start()
            except Exception as e:
                print(f"[MessageStream] Accept error: {e}")

    def stop(self):
        """
        Stops the server and closes the socket.
        """
        self.running = False
        self.server_socket.close()

    def _handle_client(self, conn: socket.socket, addr: tuple):
        """
        Handles a single client connection.

        Args:
            conn (socket.socket): The client socket.
            addr (tuple): The client (IP, port).
        """
        buffer = b""
        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"[MessageStream] Connection closed by {addr}")
                    break

                buffer += data

                while True:
                    if buffer.count(b' ') < 2:
                        break

                    try:
                        first_space = buffer.index(b' ')
                        second_space = buffer.index(b' ', first_space + 1)
                        payload_len = int(buffer[first_space + 1:second_space].decode())
                    except ValueError:
                        print(f"[MessageStream] Malformed header from {addr}")
                        return

                    payload_start = second_space + 1
                    total_len = payload_start + payload_len + 1  # +1 for newline

                    if len(buffer) < total_len:
                        break

                    if buffer[total_len - 1] != ord('\n'):
                        print(f"[MessageStream] Invalid message ending from {addr}")
                        return

                    full_msg = buffer[:total_len]
                    buffer = buffer[total_len:]

                    # Call the user-provided handler
                    self.handler(full_msg, addr, conn)

        except Exception as e:
            print(f"[MessageStream] Client error ({addr}): {e}")
        finally:
            conn.close()
            print(f"[MessageStream] Disconnected {addr}")

def handle_connections(self):
    from message_stream_threaded import MessageStream  # your new class with threading support

    addr = config['address']
    connection_port = config['typing_feature']['server_connection_port']

    def handle_client(msg: bytes, client_addr: tuple, conn: socket.socket):
        data = parse_msg(msg)[2]
        data['subscriberIP'] = client_addr[0]

        connection_response = messenger_pb2.ConnectionResponse()

        if data['subscriberIP'] in [subscriber['subscriberIP'] for subscriber in self.subscriber_list]:
            connection_response.result = messenger_pb2.ConnectionResponse.Result.IS_ALREADY_CONNECTED_ERROR
            yellow(f'Subscriber {":".join(map(str, client_addr))} already subscribed to list.')
        else:
            connection_response.result = messenger_pb2.ConnectionResponse.Result.CONNECTED
            green(f"\nTYPING_INDICATOR connection established with: {data}")
            self.subscriber_list.append(data)

        try:
            conn.send(serialize_msg('CONNECTION_RESPONSE', connection_response))
        except Exception as e:
            yellow(f"Failed to send response to {client_addr}: {e}")
        finally:
            conn.close()

    stream = MessageStream(addr, connection_port, handler=handle_client)
    blue(f"Listening for typing_connections on {addr}:{connection_port}...")
    stream.start()

#Handle Ping, Hangup and Resend in handle client:
def handle_client(msg: bytes, addr: tuple, conn: socket.socket):
    msg_parts = msg.split(b' ', 2)
    if len(msg_parts) < 3:
        print(f"Malformed message from {addr}")
        conn.close()
        return

    msg_type = msg_parts[0].decode()
    payload = msg_parts[2][:-1]  # Remove newline

    if msg_type == "PING":
        conn.send(b'PONG 0 \n')
        print(f"PING -> PONG sent to {addr}")

    elif msg_type == "HANGUP":
        print(f"Client {addr} requested hangup.")
        # You might remove from subscriber_list here
        conn.send(b'HANGUP_ACK 0 \n')
        conn.close()

    elif msg_type == "RESEND":
        print(f"Client {addr} requested RESEND.")
        # You might resend last known state
        events = self.format_typing_events_list()
        conn.send(serialize_msg("TYPING_EVENTS", events))

    elif msg_type == "CONNECTION_REQUEST":
        # Your existing connection logic here
        ...

    else:
        print(f"Unknown message type '{msg_type}' from {addr}")
        conn.close()

# client tries to connect again
self.active_clients = set()

if addr in self.active_clients:
    print(f"[MessageStream] Duplicate client {addr} rejected")
    conn.close()
    return
self.active_clients.add(addr)

self.active_clients.discard(addr)