#!/usr/bin/env python3
"""
Simple test script to verify chat functionality
Run the server first, then this client test
"""

import sys
import os
import time
import threading

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from client.chat import ChatClient
from protobuf import messenger_pb2

def test_chat_client():
    print("=== Chat Client Test ===")
    
    # Create a chat client
    user_id = "test_user_1"
    server_id = "homeserver1"
    
    print(f"Creating chat client for {user_id}@{server_id}")
    chat_client = ChatClient(user_id=user_id, server_id=server_id)
    
    if not chat_client.is_connected:
        print("❌ Failed to connect to chat server")
        print("Make sure the chat server is running first!")
        return False
    
    print("✅ Successfully connected to chat server")
    
    # Test sending a text message to another user
    print("\n--- Testing text message to user ---")
    success = chat_client.send_message_to_user(
        text_content="Hello from test client!",
        recipient_user_id="test_user_2",
        recipient_server_id="homeserver1"
    )
    
    if success:
        print("✅ Text message sent successfully")
    else:
        print("❌ Failed to send text message")
    
    # Test sending a message to a group
    print("\n--- Testing text message to group ---")
    success = chat_client.send_message_to_group(
        text_content="Hello group from test client!",
        recipient_group_id="test_group",
        recipient_server_id="homeserver1"
    )
    
    if success:
        print("✅ Group message sent successfully")
    else:
        print("❌ Failed to send group message")
    
    # Test sending a live location
    print("\n--- Testing live location message ---")
    live_location = messenger_pb2.LiveLocation()
    live_location.user.userId = user_id
    live_location.user.serverId = server_id
    live_location.timestamp = time.time()
    live_location.expiry_at = time.time() + 3600  # Expires in 1 hour
    live_location.location.latitude = 48.2627  # Munich coordinates
    live_location.location.longitude = 11.6742
    
    success = chat_client.send_live_location(
        live_location=live_location,
        recipient_user_id="test_user_2",
        recipient_server_id="homeserver1"
    )
    
    if success:
        print("✅ Live location sent successfully")
    else:
        print("❌ Failed to send live location")
    
    # Wait a bit for any responses
    print("\n--- Waiting for responses (5 seconds) ---")
    time.sleep(5)
    
    # Clean up
    chat_client.close()
    print("✅ Chat client closed successfully")
    
    return True

def main():
    print("Chat Functionality Test")
    print("Make sure to start the chat server first with: python -m server.main")
    print("Press Enter to continue or Ctrl+C to cancel...")
    
    try:
        input()
    except KeyboardInterrupt:
        print("\nTest cancelled")
        return
    
    success = test_chat_client()
    
    if success:
        print("\n🎉 Chat test completed successfully!")
    else:
        print("\n❌ Chat test failed!")

if __name__ == "__main__":
    main()
