import socket

# Start Echo server and then the chat client


def chat_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect(("localhost", 8090))
            while True:
                msg = input("You (exit to leave): ")
                if msg.lower() == 'exit':
                    break
                try:
                    s.sendall(msg.encode('ASCII'))
                except UnicodeEncodeError as e:
                    print(e)
                    print("Only ASCII characters can be used. Ü, Ä, Ö and more can't be sent.\n")
                    continue

                data = s.recv(1024)
                if not data:
                    print("Server closed the connection.")
                    break
                print("Server:", data.decode('ASCII'))

        except ConnectionRefusedError as e:
            print(e)
            print("\nPlease start the echo server script!\n")


if __name__ == '__main__':
    chat_client()
