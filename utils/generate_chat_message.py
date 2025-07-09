import time
from protobuf import messenger_pb2


def generate_chat_message(
    author_user_id: str,
    author_server_id: str,
    recipient: dict = None,
    content: dict = None,
) -> messenger_pb2.ChatMessage:
    """
    Construct a ChatMessage protobuf object with generated snowflake ID.
    
    Args:
        author_user_id (str): Author's user ID.
        author_server_id (str): Author's server ID.
        recipient (dict): Optional. One of:
            - {'user': {'userId': str, 'serverId': str}}
            - {'group': {'groupId': str, 'serverId': str}}
            - {'userOfGroup': {'user': {...}, 'group': {...}}}
        content (dict): Optional. One of:
            - {'textContent': str}
            - {'document': messenger_pb2.Document}
            - {'translation': messenger_pb2.Translation}
            - {'live_location': messenger_pb2.LiveLocation}
        message_counter (int): Optional override for internal sequence generation.
    
    Returns:
        messenger_pb2.ChatMessage: A complete ChatMessage object.
    """

    # --- Generate Snowflake ID ---
    def generate_snowflake(user_id: str) -> int:
        """
        Generate a simple snowflake using timestamp and user hash only.
        Layout: [timestamp (48 bits)][user_hash (16 bits)] = 64 bits
        """
        timestamp_ms = int(time.time() * 1000)  # 48 bits
        user_hash = hash(user_id) & 0xFFFF      # 16 bits
        return (timestamp_ms << 16) | user_hash

    # --- Construct Protobuf ---
    msg = messenger_pb2.ChatMessage()
    msg.messageSnowflake = generate_snowflake(author_user_id)

    # Author
    msg.author.userId = author_user_id
    msg.author.serverId = author_server_id

    # Recipient
    if recipient:
        if 'user' in recipient:
            msg.user.userId = recipient['user']['userId']
            msg.user.serverId = recipient['user']['serverId']
        elif 'group' in recipient:
            msg.group.groupId = recipient['group']['groupId']
            msg.group.serverId = recipient['group']['serverId']
        elif 'userOfGroup' in recipient:
            uog = recipient['userOfGroup']
            msg.userOfGroup.user.userId = uog['user']['userId']
            msg.userOfGroup.user.serverId = uog['user']['serverId']
            msg.userOfGroup.group.groupId = uog['group']['groupId']
            msg.userOfGroup.group.serverId = uog['group']['serverId']

    # Content
    if content:
        if 'textContent' in content:
            msg.textContent = content['textContent']
        elif 'document' in content:
            msg.document.CopyFrom(content['document'])
        elif 'translation' in content:
            msg.translation.CopyFrom(content['translation'])
        elif 'live_location' in content:
            msg.live_location.CopyFrom(content['live_location'])
        else:
            raise ValueError(f"Unsupported content type: {list(content.keys())}")

    return msg
