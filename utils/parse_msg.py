from google.protobuf.json_format import MessageToDict
from protobuf import messenger_pb2
from .serialize_msg import serialize_msg


# Mapping message names to their corresponding protobuf classes. This allows for dynamic parsing of messages based on their names.
message_classes = {
    'DISCOVER_SERVER': messenger_pb2.DiscoverServer,
    'SERVER_ANNOUNCE': messenger_pb2.ServerAnnounce,
    'CONNECT_CLIENT': messenger_pb2.ConnectClient,
    'CONNECTED': messenger_pb2.ConnectResponse,
    'HANGUP': messenger_pb2.HangUp,
    'TYPING_EVENT': messenger_pb2.TypingEvent,
    'TYPING_EVENTS': messenger_pb2.TypingEvents,
    'LIVE_LOCATION': messenger_pb2.LiveLocation,
    'LIVE_LOCATIONS': messenger_pb2.LiveLocations,
    'MESSAGE': messenger_pb2.ChatMessage,
    'MESSAGE_ACK': messenger_pb2.ChatMessageResponse,
    'PING': messenger_pb2.Ping,
    'PONG': messenger_pb2.Pong,
    'UNSUPPORTED_MESSAGE': messenger_pb2.UnsupportedMessage,
    'DOWNLOADING_DOCUMENT': messenger_pb2.DownloadingDocument,
    'TRANSLATED': messenger_pb2.Translated,
}



def parse_msg(data : bytes) -> tuple[str, int, dict]:
    """
    Parses a byte string containing a message name, size, and payload, optionally decoding the payload using a provided protobuf class.
    Args:
        data (bytes): The input byte string, expected to be formatted as `b'<message_name>  <size>  <payload>\\n'`.
    Returns:
        tuple[str, int, dict]: A tuple containing:
            - message_name (str): The decoded message name.
            - size (int): The decoded size as a string.
            - dict_payload (dict): The payload parsed into a dictionary if `pb_class` is provided, otherwise an empty dictionary.
    """

    message_name, size, payload = data.split(b' ', 2)

    message_name = message_name.decode('ascii')
    size = int(size.decode('ascii'))
  
    # Converts payload into dictionary
    payload = payload.rstrip(b'\n') # Remove \n from last part of the message
    if message_classes.get(message_name) is None:
        raise ValueError({'type': 'Parsing Error', 'message': f'Unknown message type: \'{message_name}\'. Couldnt map the message_name to any of our defined protobuf classes during parsing. Please check the message_name of the protobuf message or check the mapping in the parse_msg function.'})
    else:
        parsed_instance = message_classes.get(message_name)()  # Get the protobuf class for the message name
        parsed_instance.ParseFromString(payload)
        dict_payload = MessageToDict(parsed_instance)

    return message_name, size, dict_payload