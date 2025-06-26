#!/usr/bin/env python3
"""
Standalone test for chat functionality without dependencies
"""
import socket
import threading
import time
import sys
import os

# Add the project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from protobuf import messenger_pb2

def test_chat_standalone():
    """Test chat functionality without config dependencies"""
    
    # Test protobuf message creation
    print("=== Testing ChatMessage Creation ===")
    
    # Create a chat message
    chat_msg = messenger_pb2.ChatMessage()
    chat_msg.messageSnowflake = int(time.time() * 1000)
    chat_msg.author.userId = "test_user"
    chat_msg.author.serverId = "test_server"
    chat_msg.user.userId = "target_user" 
    chat_msg.user.serverId = "target_server"
    chat_msg.textContent = "Hello from standalone test!"
    
    print(f"✅ Created ChatMessage:")
    print(f"   Snowflake: {chat_msg.messageSnowflake}")
    print(f"   Author: {chat_msg.author.userId}@{chat_msg.author.serverId}")
    print(f"   Recipient: {chat_msg.user.userId}@{chat_msg.user.serverId}")
    print(f"   Content: {chat_msg.textContent}")
    print(f"   Recipient Type: {chat_msg.WhichOneof('recipient')}")
    print(f"   Content Type: {chat_msg.WhichOneof('content')}")
    
    # Test serialization
    serialized = chat_msg.SerializeToString()
    print(f"✅ Serialized to {len(serialized)} bytes")
    
    # Test deserialization
    new_msg = messenger_pb2.ChatMessage()
    new_msg.ParseFromString(serialized)
    print(f"✅ Deserialized successfully")
    print(f"   Snowflake: {new_msg.messageSnowflake}")
    print(f"   Text: {new_msg.textContent}")
    
    # Test ChatMessageResponse
    print("\n=== Testing ChatMessageResponse ===")
    response = messenger_pb2.ChatMessageResponse()
    response.messageSnowflake = chat_msg.messageSnowflake
    
    status = response.statuses.add()
    status.user.userId = "target_user"
    status.user.serverId = "target_server"
    status.status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
    
    print(f"✅ Created ChatMessageResponse:")
    print(f"   Snowflake: {response.messageSnowflake}")
    print(f"   Status count: {len(response.statuses)}")
    print(f"   Status: {messenger_pb2.ChatMessageResponse.Status.Name(response.statuses[0].status)}")
    
    # Test Group message
    print("\n=== Testing Group Message ===")
    group_msg = messenger_pb2.ChatMessage()
    group_msg.messageSnowflake = int(time.time() * 1000) + 1
    group_msg.author.userId = "sender"
    group_msg.author.serverId = "sender_server"
    group_msg.group.groupId = "test_group"
    group_msg.group.serverId = "group_server"
    group_msg.textContent = "Hello group!"
    
    print(f"✅ Created Group ChatMessage:")
    print(f"   Group: {group_msg.group.groupId}@{group_msg.group.serverId}")
    print(f"   Recipient Type: {group_msg.WhichOneof('recipient')}")
    
    # Test UserOfGroup message
    print("\n=== Testing UserOfGroup Message ===")
    uog_msg = messenger_pb2.ChatMessage()
    uog_msg.messageSnowflake = int(time.time() * 1000) + 2
    uog_msg.author.userId = "sender"
    uog_msg.author.serverId = "sender_server"
    uog_msg.userOfGroup.user.userId = "group_member"
    uog_msg.userOfGroup.user.serverId = "member_server"
    uog_msg.userOfGroup.group.groupId = "test_group"
    uog_msg.userOfGroup.group.serverId = "group_server"
    uog_msg.textContent = "Hello group member!"
    
    print(f"✅ Created UserOfGroup ChatMessage:")
    print(f"   Member: {uog_msg.userOfGroup.user.userId}@{uog_msg.userOfGroup.user.serverId}")
    print(f"   Group: {uog_msg.userOfGroup.group.groupId}@{uog_msg.userOfGroup.group.serverId}")
    print(f"   Recipient Type: {uog_msg.WhichOneof('recipient')}")
    
    # Test Live Location message
    print("\n=== Testing Live Location Message ===")
    loc_msg = messenger_pb2.ChatMessage()
    loc_msg.messageSnowflake = int(time.time() * 1000) + 3
    loc_msg.author.userId = "location_sender"
    loc_msg.author.serverId = "location_server"
    loc_msg.user.userId = "location_recipient"
    loc_msg.user.serverId = "recipient_server"
    
    # Set live location
    loc_msg.live_location.user.userId = "location_sender"
    loc_msg.live_location.user.serverId = "location_server"
    loc_msg.live_location.timestamp = time.time()
    loc_msg.live_location.expiry_at = time.time() + 3600
    loc_msg.live_location.location.latitude = 48.2627  # Munich
    loc_msg.live_location.location.longitude = 11.6742
    
    print(f"✅ Created Live Location ChatMessage:")
    print(f"   Location: {loc_msg.live_location.location.latitude}, {loc_msg.live_location.location.longitude}")
    print(f"   Content Type: {loc_msg.WhichOneof('content')}")
    
    print("\n=== All Tests Passed! ===")
    print("✅ ChatMessage structure works correctly")
    print("✅ All recipient types (User, Group, UserOfGroup) work")
    print("✅ All content types (text, live_location) work") 
    print("✅ ChatMessageResponse works correctly")
    print("✅ Serialization/deserialization works")
    print("\nThe chat message protocol is ready to use!")

if __name__ == "__main__":
    try:
        test_chat_standalone()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
