import socket
import messenger_pb2

server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
private_ip = socket.gethostbyname(socket.gethostname())



messenger = messenger_pb2.TypingEvents()
messenger.typing_events.add(userId="user123", timestamp=1633072800.0)
