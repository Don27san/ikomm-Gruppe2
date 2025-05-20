import socket
import time
import threading


# TODO: broadcast and echo_server is run externally
def echo_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    print("Echo Server started and listening for connections.")
    
    try:
        while True:
            server_socket.settimeout(1)  # Timeout for the accept call
            try:
                conn, addr = server_socket.accept()
                print(f"Connected to {addr}")
                try:
                    while True:
                        data = conn.recv(100000)
                        if not data:
                            break
                        conn.sendall(data)  # Echo the received data back to the client
                finally:
                    conn.close()
                    print("Connection closed.")
            except socket.timeout:
                continue  # No connection within timeout period, loop back to accept
    except KeyboardInterrupt:
        print("Server is shutting down...")
    finally:
        server_socket.close()
        print("Server shut down.")


def measure_rtt(host, port, message_length):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    message = 'A' * message_length  # Create a message of 'A' repeated to the specified length

    # Send the message and measure the RTT
    start_time = time.time()
    client_socket.sendall(message.encode('ASCII'))
    response = client_socket.recv(100000)  # Assuming the echo will not exceed 1024 bytes
    end_time = time.time()

    client_socket.close()

    rtt = end_time - start_time
    print(f"RTT for message of length {message_length}: {rtt * 1000:.2f} ms")


if __name__ == '__main__':
    server_host = 'localhost'
    server_port = 9999
    
    # Start server in a background thread
    server_thread = threading.Thread(target=echo_server, args=(server_host, server_port))
    server_thread.daemon = True  # Ensure that the thread will exit when the main program does
    server_thread.start()
    print("Server thread started. Enter the message length as an integer.\n"
          "When the server and client are run locally, the message length should not highly impact the RTT.\n"
          "When running the server and client on different machines, the RTT increases with increasing message length."
          "\n========================================================================================================\n")

    try:
        while True:
            user_input = input("Enter the message length or type 'quit' to exit: \n")
            if user_input.lower() == "quit":
                print("Exiting...")
                break
            try:
                message_length = int(user_input)
                if message_length > 100000:
                    print("Message length must be less than 100001.")
                elif message_length > 0:
                    measure_rtt(server_host, server_port, message_length)
                else:
                    print("Message length must be greater than 0.")
            except ValueError:
                print("Please enter a valid integer for message length.")
    except KeyboardInterrupt:
        print("Program interrupted, exiting...")
    finally:
        print("Cleanup complete, program terminated.")
