from typing_extensions import Literal
from google.protobuf.message import Message
from typing import Optional

MessageName = Literal[
    'DISCOVER_SERVER',
    'SERVER_ANNOUNCE',
    'CONNECT_CLIENT',
    'CONNECTED',
    'HANGUP',
    'TYPING_EVENT',
    'TYPING_EVENTS',
    'LIVE_LOCATION',
    'LIVE_LOCATIONS',
    'CHAT_MESSAGE',
    'CHAT_MESSAGE_RESPONSE',
    'PING',
    'PONG',
    'UNSUPPORTED_MESSAGE',
]

def serialize_msg(message_name: MessageName, payload: Optional[Message] = None) -> bytes:
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