#!/usr/bin/env python3
"""
Test script for the chat functionality
"""
import time
import threading
from client.chat import ChatClient
from protobuf import messenger_pb2

def test_chat_client():
    """Test the chat client functionality"""
    print("Starting Chat Client Test...")
    
    # Create a test client
    client = ChatClient(user_id="test_user", server_id="homeserver1")
    
    if not client.is_connected:
        print("Failed to connect to server. Make sure chat_server.py is running.")
        return
    
    time.sleep(1)  # Let connection stabilize
    
    # Test 1: Send message to user
    print("\n=== Test 1: Sending message to user ===")
    success = client.send_message_to_user(
        text_content="Hello from test client!",
        recipient_user_id="target_user",
        recipient_server_id="homeserver1"
    )
    print(f"Message sent successfully: {success}")
    
    time.sleep(1)
    
    # Test 2: Send message to group
    print("\n=== Test 2: Sending message to group ===")
    success = client.send_message_to_group(
        text_content="Hello group!",
        recipient_group_id="test_group",
        recipient_server_id="homeserver1"
    )
    print(f"Group message sent successfully: {success}")
    
    time.sleep(1)
    
    # Test 3: Send live location
    print("\n=== Test 3: Sending live location ===")
    live_location = messenger_pb2.LiveLocation()
    live_location.user.userId = "test_user"
    live_location.user.serverId = "homeserver1"
    live_location.timestamp = time.time()
    live_location.expiry_at = time.time() + 3600  # Expires in 1 hour
    live_location.location.latitude = 48.2627  # Munich, Germany
    live_location.location.longitude = 11.6742
    
    success = client.send_live_location(
        live_location=live_location,
        recipient_user_id="target_user",
        recipient_server_id="homeserver1"
    )
    print(f"Live location sent successfully: {success}")
    
    # Keep client running for a bit to receive responses
    print("\nWaiting for responses...")
    time.sleep(3)
    
    client.close()
    print("Test completed!")

if __name__ == "__main__":
    try:
        test_chat_client()
    except KeyboardInterrupt:
        print("\nTest interrupted by user")
    except Exception as e:
        print(f"Test failed with error: {e}")
