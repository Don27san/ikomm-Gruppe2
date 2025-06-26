#!/usr/bin/env python3
"""
Test recipient types
"""
from protobuf import messenger_pb2

def test_recipient_types():
    print("Testing recipient types...")
    
    # Test user recipient
    user_msg = messenger_pb2.ChatMessage()
    user_msg.user.userId = "test_user"
    user_msg.user.serverId = "test_server"
    print(f"User recipient type: {user_msg.WhichOneof('recipient')}")
    
    # Test group recipient
    group_msg = messenger_pb2.ChatMessage()
    group_msg.group.groupId = "test_group"
    group_msg.group.serverId = "test_server"
    print(f"Group recipient type: {group_msg.WhichOneof('recipient')}")
    
    # Test userOfGroup recipient
    uog_msg = messenger_pb2.ChatMessage()
    uog_msg.userOfGroup.user.userId = "test_user"
    uog_msg.userOfGroup.user.serverId = "test_server"
    uog_msg.userOfGroup.group.groupId = "test_group"
    uog_msg.userOfGroup.group.serverId = "test_server"
    print(f"UserOfGroup recipient type: {uog_msg.WhichOneof('recipient')}")

if __name__ == "__main__":
    test_recipient_types()
