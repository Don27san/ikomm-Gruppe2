# Chat Message Implementation

This implementation provides a complete chat messaging system according to the specified protocol requirements. It supports text messages, live location sharing, and group messaging with proper routing and acknowledgments.

## Protocol Compliance

The implementation follows the specified message protocol:

### ChatMessage Structure

- `messageSnowflake`: Unique message identifier
- `author`: User who sent the message
- `recipient`: Can be User, Group, or UserOfGroup
- `content`: Can be textContent or live_location

### ChatMessageResponse Structure

- `messageSnowflake`: Matches the original message
- `statuses`: Array of delivery statuses for each recipient

## Key Features

1. **Message Routing**: Proper routing based on recipient type (User/Group/UserOfGroup)
2. **Group Message Handling**: Groups are split into individual UserOfGroup messages
3. **Live Location Support**: Integrated with your group's live location feature
4. **Server Communication**: Framework for inter-server message relay
5. **Acknowledgments**: ChatMessageResponse with delivery status tracking

## Files Updated/Created

### Server Side

- `server/chat_server.py`: Main chat server implementation
- `server/main.py`: Updated to include chat service
- `protobuf/messenger.proto`: Updated with proper message structures
- `config.py`: Added chat service configuration
- `utils/protobuf_payloads.py`: Added chat service to announcements

### Client Side

- `client/chat.py`: Complete chat client with message handling
- `test_chat.py`: Test script for validation

## Usage

### Starting the Server

```bash
cd /path/to/ikomm-Gruppe2
python -m server.main
```

### Using the Chat Client

```python
from client.chat import ChatClient
from protobuf import messenger_pb2

# Create client
client = ChatClient(user_id="user123", server_id="homeserver1")

# Send text message to user
client.send_message_to_user(
    text_content="Hello!",
    recipient_user_id="target_user",
    recipient_server_id="homeserver1"
)

# Send message to group
client.send_message_to_group(
    text_content="Hello group!",
    recipient_group_id="my_group",
    recipient_server_id="homeserver1"
)

# Send live location
live_location = messenger_pb2.LiveLocation()
live_location.user.userId = "user123"
live_location.user.serverId = "homeserver1"
live_location.timestamp = time.time()
live_location.expiry_at = time.time() + 3600
live_location.location.latitude = 48.2627
live_location.location.longitude = 11.6742

client.send_live_location(
    live_location=live_location,
    recipient_user_id="target_user",
    recipient_server_id="homeserver1"
)
```

### Testing

```bash
# Start server in one terminal
python -m server.main

# Run test in another terminal
python test_chat.py
```

## Message Flow

1. **Client → Server**: Client sends ChatMessage
2. **Server Processing**:
   - Validates message structure
   - Routes based on recipient type
   - For Groups: splits into UserOfGroup messages
   - For local users: delivers directly
   - For remote servers: relays (framework in place)
3. **Server → Client**: Returns ChatMessageResponse with delivery status

## Integration with Live Location

The chat system is designed to work seamlessly with your live location feature:

- Live location messages use the same ChatMessage structure
- Location data is embedded in the `live_location` field
- All routing and acknowledgment logic applies to location messages

## Configuration

Chat service configuration in `config.py`:

```python
'chat_feature': {
    'server_port': 6001,  # Chat server port
}
```

The chat service is automatically announced during server discovery with the "CHAT" feature name.

## Protocol Rules Implemented

✅ **Message Validation**: Validates author/group ownership for inter-server messages  
✅ **User Routing**: Direct delivery to local users, relay to remote servers  
✅ **Group Handling**: Splits group messages into UserOfGroup messages  
✅ **UserOfGroup Processing**: Delivers to individual group members  
✅ **Error Handling**: Proper error responses for invalid recipients  
✅ **Acknowledgments**: ChatMessageResponse with detailed delivery status

## Future Enhancements

1. **Inter-server Communication**: Currently framework is in place, needs actual TCP connections to other servers
2. **Persistence**: Add database storage for offline message delivery
3. **Authentication**: Add user authentication and authorization
4. **Encryption**: Add end-to-end encryption for messages
5. **File Attachments**: Extend content types beyond text and location

## Troubleshooting

1. **Connection Issues**: Ensure server is running and port 6001 is available
2. **Import Errors**: Make sure protobuf files are compiled (`protoc` command)
3. **Message Parsing**: Check that both client and server use the same protobuf version
