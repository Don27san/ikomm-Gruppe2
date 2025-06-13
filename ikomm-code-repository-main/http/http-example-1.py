import socket


def web_client():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect(("ik.lkn.ei.tum.de", 8000))
            s.sendall("GET /helloworld.txt HTTP/1.1\r\nHost: ik.lkn.ei.tum.de\r\n\r\n".encode("ASCII"))
            data = s.recv(10000)
            print(data.decode("ASCII"))
    except socket.gaierror as e:
        print(e)
        print("Check if connection to the Internet has been established.")
    except TimeoutError as e:
        print(e)
        print("Check if you are connected to Eduroam!\n")


if __name__ == '__main__':
    web_client()
