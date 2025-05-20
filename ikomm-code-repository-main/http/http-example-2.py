import socket

# Define the server address and port
HOST = '127.0.0.1'  # Localhost
PORT = 8080         # Port to listen on

# Create a socket object
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
    # Bind the socket to the address and port
    server_socket.bind((HOST, PORT))
    # Listen for incoming connections (max 1 connection in the queue)
    server_socket.listen(1)
    
    print(f"Server is running on http://{HOST}:{PORT}.\nOpen the website by clicking on the link above!")

    # Wait for a client connection
    while True:
        client_connection, client_address = server_socket.accept()
        with client_connection:
            print(f"Connected by {client_address}")

            # Receive the request data from the client
            request_data = client_connection.recv(1024).decode()
            print(f"Request data:\n{request_data}")

            # Prepare the HTTP response
            http_response = """\
HTTP/1.1 200 OK

<!DOCTYPE html>
<html>
<head>
    <title>Basic HTTP Server</title>
</head>
<body>
    <h1>Hello, World!</h1>
    <p>This is a simple HTTP server example using Python's socket library.</p>
</body>
</html>
"""

            # Send the HTTP response
            client_connection.sendall(http_response.encode())

            # Close the client connection
            client_connection.close()
