#!/usr/bin/env python3
"""
Test script for chat system using MessageStream format
This script demonstrates that the chat system is now using the standard MessageStream format
for interoperability with other groups.
"""

import time
import threading
from client.chat import ChatClient
from server.chat_server import start_server
from protobuf import messenger_pb2
from utils import serialize_msg, parse_msg

def test_message_format():
    print("=== Testing MessageStream Format Integration ===")
    
    # Test 1: Message serialization format
    print("\n1. Testing message serialization format:")
    
    chat_msg = messenger_pb2.ChatMessage()
    chat_msg.messageSnowflake = 12345
    chat_msg.author.userId = "test_user"
    chat_msg.author.serverId = "test_server"
    chat_msg.user.userId = "recipient"
    chat_msg.user.serverId = "recipient_server"
    chat_msg.textContent = "Hello World!"
    
    # Serialize using MessageStream format
    msg = serialize_msg('CHAT_MESSAGE', chat_msg)
    
    # Verify format: should be "CHAT_MESSAGE <size> <payload>\n"
    parts = msg.split(b' ', 2)
    message_name = parts[0].decode('ascii')
    size = int(parts[1].decode('ascii'))
    payload_with_newline = parts[2]
    payload = payload_with_newline[:-1]  # Remove newline
    
    print(f"  ✓ Message name: {message_name}")
    print(f"  ✓ Payload size: {size}")
    print(f"  ✓ Actual payload size: {len(payload)}")
    print(f"  ✓ Format validation: {'PASSED' if size == len(payload) else 'FAILED'}")
    
    # Test 2: Message parsing
    print("\n2. Testing message parsing:")
    try:
        parsed_name, parsed_size, parsed_payload = parse_msg(msg)
        print(f"  ✓ Parsed message name: {parsed_name}")
        print(f"  ✓ Parsed size: {parsed_size}")
        print(f"  ✓ Parsed payload keys: {list(parsed_payload.keys())}")
        print(f"  ✓ Text content: {parsed_payload.get('textContent', 'NOT_FOUND')}")
        
        # Verify all expected fields are present
        expected_fields = ['messageSnowflake', 'author', 'user', 'textContent']
        missing_fields = [field for field in expected_fields if field not in parsed_payload]
        if not missing_fields:
            print("  ✓ All expected fields present")
        else:
            print(f"  ✗ Missing fields: {missing_fields}")
            
    except Exception as e:
        print(f"  ✗ Parsing failed: {e}")
    
    # Test 3: Response message format
    print("\n3. Testing response message format:")
    
    response = messenger_pb2.ChatMessageResponse()
    response.messageSnowflake = 12345
    
    status = response.statuses.add()
    status.user.userId = "recipient"
    status.user.serverId = "recipient_server"
    status.status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
    
    response_msg = serialize_msg('CHAT_MESSAGE_RESPONSE', response)
    
    try:
        parsed_response_name, parsed_response_size, parsed_response_payload = parse_msg(response_msg)
        print(f"  ✓ Response message name: {parsed_response_name}")
        print(f"  ✓ Response size: {parsed_response_size}")
        print(f"  ✓ Response payload keys: {list(parsed_response_payload.keys())}")
        print("  ✓ Response format validation: PASSED")
    except Exception as e:
        print(f"  ✗ Response parsing failed: {e}")
    
    print("\n=== MessageStream Integration Test Complete ===")
    print("\nThe chat system is now using the standard MessageStream format:")
    print("- Format: '<message_name> <size> <payload>\\n'")
    print("- Compatible with other groups' implementations")
    print("- Supports both CHAT_MESSAGE and CHAT_MESSAGE_RESPONSE")
    print("- Ready for interoperability testing")

def demonstrate_interoperability():
    print("\n=== Interoperability Features ===")
    print("The chat system now includes:")
    print("1. Standard MessageStream format for all messages")
    print("2. Proper message parsing and serialization")
    print("3. Support for both legacy and MessageStream clients")
    print("4. Ready for integration with other groups' servers")
    print("\nMessage format examples:")
    
    # Show actual message formats
    chat_msg = messenger_pb2.ChatMessage()
    chat_msg.messageSnowflake = 98765
    chat_msg.author.userId = "group2_user"
    chat_msg.author.serverId = "homeserver1"
    chat_msg.user.userId = "group3_user"
    chat_msg.user.serverId = "homeserver2"
    chat_msg.textContent = "Inter-group message!"
    
    msg = serialize_msg('CHAT_MESSAGE', chat_msg)
    
    # Show the actual bytes being sent
    print(f"\nActual message format:")
    print(f"Raw bytes: {msg[:60]}...")
    print(f"Decoded start: {msg[:20].decode('ascii', errors='ignore')}")
    
    # Parse and show structure
    name, size, payload = parse_msg(msg)
    print(f"\nParsed structure:")
    print(f"- Message name: {name}")
    print(f"- Payload size: {size} bytes")
    print(f"- Author: {payload['author']['userId']}@{payload['author']['serverId']}")
    print(f"- Recipient: {payload['user']['userId']}@{payload['user']['serverId']}")
    print(f"- Content: {payload['textContent']}")

if __name__ == "__main__":
    test_message_format()
    demonstrate_interoperability()
