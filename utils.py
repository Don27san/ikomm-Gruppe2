from protobuf import messenger_pb2
from config import config
from google.protobuf.json_format import MessageToDict
from google.protobuf.message import Message
from typing import Optional, Type


# Server_Announce Payload
server_announce = messenger_pb2.ServerAnnounce()
server_announce.serverId="2"
server_announce.feature.add(featureName="TYPING_INDICATOR", port=config['typing_feature']['server_connection_port'])
server_announce.feature.add(featureName="LIVE_LOCATION", port=config['location_feature']['server_connection_port'])

# Connect_Client Payload
connect_client = messenger_pb2.ConnectClient()
connect_client.user.userId = "user123" #Static value, must be replaced if necessary
connect_client.user.serverId = "server456" #Static value, must be replaced if necessary
connect_client.typingPort = config['typing_feature']['client_typing_port']

# Typing_Event Payload
typing_event = messenger_pb2.TypingEvent()
typing_event.user.userId = "user123" #Static value, must be replaced if necessary
typing_event.user.serverId = "server456" #Static value, must be replaced if necessary



def red(string):
    print('\033[31m' + string + '\033[0m')

def blue(string):
    print('\033[34m' + string + '\033[0m')

def green(string):
    print('\033[32m' + string + '\033[0m')

def yellow(string):
    print('\033[93m' + string + '\033[0m')








# Serializes data which we want to send
def serialize_data(message_name: str, payload: Optional[Message] = None) -> bytes:
    """
    Serializes a message for transmission by combining a message name and an optional payload.
    Args:
        message_name (str): The name of the message `'SERVER_ANNOUNCE', 'DISCOVER_SERVER', etc`.
        payload (Optional[google.protobuf.message.Message]): An optional protobuf message to serialize. 
            If None, no payload is included.
    Returns:
        bytes: The serialized message in the format: 
            b'<message_name> <payload_length> <payload_bytes>\\n'
    Example:
        >>> serialize_data('SERVER_ANNOUNCE', payload)
        b'SERVER_ANNOUNCE 42 <payload_bytes>\\n'   
    """
    body = b'' if payload is None else payload.SerializeToString()
    data = f'{message_name} {len(body)} '.encode('ascii') + body + b'\n'
    return data



def parse_data(data : bytes, pb_class : Type[Message] | None = None) -> tuple[str, int, dict]:
    """
    Parses a byte string containing a message name, size, and payload, optionally decoding the payload using a provided protobuf class.
    Args:
        data (bytes): The input byte string, expected to be formatted as `b'<message_name>  <size>  <payload>\\n'`.
        pb_class (Type[Message] | None, optional): A protobuf message class used to parse the payload. If None, the payload is ignored and an empty dictionary is returned.
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
    if pb_class is None:
        dict_payload = {}
    else:
        parsed_instance = pb_class()
        parsed_instance.ParseFromString(payload)
        dict_payload = MessageToDict(parsed_instance)
        
    # Handle missing protobuf class error
    if size > 0 and dict_payload == {}:
        raise ValueError(f"Payload size {size} is greater than 0, but no protobuf class was provided to parse the payload.")

    return message_name, size, dict_payload


formatted = serialize_data('SERVER_ANNOUNCE', server_announce)
parsed = parse_data(formatted)
print(parsed)










