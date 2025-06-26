#!/usr/bin/env python3
"""
Simple debug test for protobuf
"""
from protobuf import messenger_pb2

def simple_test():
    print("Testing basic ChatMessage creation...")
    
    try:
        # Create a simple ChatMessage
        chat_msg = messenger_pb2.ChatMessage()
        print(f"ChatMessage created: {type(chat_msg)}")
        
        # Set snowflake
        chat_msg.messageSnowflake = 12345
        print(f"Snowflake set: {chat_msg.messageSnowflake}")
        
        # Set author
        chat_msg.author.userId = "test_user"
        chat_msg.author.serverId = "test_server"
        print(f"Author set: {chat_msg.author.userId}@{chat_msg.author.serverId}")
        
        # Set recipient - this might be where the issue is
        print("Setting recipient...")
        chat_msg.recipient.user.userId = "target_user"
        print("FAILED: recipient.user access should fail!")
        
    except Exception as e:
        print(f"Error (expected): {e}")
        print("This means we need to access the recipient field correctly...")
        
        # Try the correct way
        chat_msg.user.userId = "target_user"
        chat_msg.user.serverId = "target_server"
        print(f"User recipient set correctly: {chat_msg.user.userId}@{chat_msg.user.serverId}")
        
        # Test content
        chat_msg.textContent = "Hello, World!"
        print(f"Text content set: {chat_msg.textContent}")
        
        # Test serialization
        serialized = chat_msg.SerializeToString()
        print(f"Serialized length: {len(serialized)} bytes")
        
        # Test deserialization
        new_msg = messenger_pb2.ChatMessage()
        new_msg.ParseFromString(serialized)
        print(f"Deserialized user: {new_msg.user.userId}")
        print(f"Deserialized text: {new_msg.textContent}")
        
        print("✅ Basic protobuf test passed!")

if __name__ == "__main__":
    simple_test()
