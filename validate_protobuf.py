#!/usr/bin/env python3
"""
Validation script to ensure protobuf structures are correctly implemented
"""
import time
from protobuf import messenger_pb2

def validate_protobuf_structures():
    """Validate that all required protobuf structures work correctly"""
    print("=== Protobuf Structure Validation ===\n")
    
    # Test 1: ChatMessage with text content
    print("1. Testing ChatMessage with text content...")
    chat_msg = messenger_pb2.ChatMessage()
    chat_msg.messageSnowflake = 12345
    chat_msg.author.userId = "test_user"
    chat_msg.author.serverId = "test_server"
    chat_msg.user.userId = "target_user"
    chat_msg.user.serverId = "target_server"
    chat_msg.textContent = "Hello, World!"
    
    # Serialize and deserialize
    serialized = chat_msg.SerializeToString()
    deserialized = messenger_pb2.ChatMessage()
    deserialized.ParseFromString(serialized)
    
    assert deserialized.messageSnowflake == 12345
    assert deserialized.author.userId == "test_user"
    assert deserialized.textContent == "Hello, World!"
    print("   ✅ Text message serialization/deserialization works")
    
    # Test 2: ChatMessage with group recipient
    print("2. Testing ChatMessage with group recipient...")
    group_msg = messenger_pb2.ChatMessage()
    group_msg.messageSnowflake = 54321
    group_msg.author.userId = "sender"
    group_msg.author.serverId = "sender_server"
    group_msg.group.groupId = "test_group"
    group_msg.group.serverId = "group_server"
    group_msg.textContent = "Hello, Group!"
    
    serialized = group_msg.SerializeToString()
    deserialized = messenger_pb2.ChatMessage()
    deserialized.ParseFromString(serialized)
    
    assert deserialized.group.groupId == "test_group"
    print("   ✅ Group message serialization/deserialization works")
    
    # Test 3: ChatMessage with UserOfGroup recipient
    print("3. Testing ChatMessage with UserOfGroup recipient...")
    uog_msg = messenger_pb2.ChatMessage()
    uog_msg.messageSnowflake = 98765
    uog_msg.author.userId = "sender"
    uog_msg.author.serverId = "sender_server"
    uog_msg.userOfGroup.user.userId = "group_member"
    uog_msg.userOfGroup.user.serverId = "member_server"
    uog_msg.userOfGroup.group.groupId = "test_group"
    uog_msg.userOfGroup.group.serverId = "group_server"
    uog_msg.textContent = "Hello, Group Member!"
    
    serialized = uog_msg.SerializeToString()
    deserialized = messenger_pb2.ChatMessage()
    deserialized.ParseFromString(serialized)
    
    assert deserialized.userOfGroup.user.userId == "group_member"
    assert deserialized.userOfGroup.group.groupId == "test_group"
    print("   ✅ UserOfGroup message serialization/deserialization works")
    
    # Test 4: ChatMessage with live location
    print("4. Testing ChatMessage with live location...")
    loc_msg = messenger_pb2.ChatMessage()
    loc_msg.messageSnowflake = 11111
    loc_msg.author.userId = "location_sender"
    loc_msg.author.serverId = "location_server"
    loc_msg.user.userId = "location_recipient"
    loc_msg.user.serverId = "recipient_server"
    
    # Set live location
    loc_msg.live_location.user.userId = "location_sender"
    loc_msg.live_location.user.serverId = "location_server"
    loc_msg.live_location.timestamp = time.time()
    loc_msg.live_location.expiry_at = time.time() + 3600
    loc_msg.live_location.location.latitude = 48.2627
    loc_msg.live_location.location.longitude = 11.6742
    
    serialized = loc_msg.SerializeToString()
    deserialized = messenger_pb2.ChatMessage()
    deserialized.ParseFromString(serialized)
    
    assert abs(deserialized.live_location.location.latitude - 48.2627) < 0.001
    assert abs(deserialized.live_location.location.longitude - 11.6742) < 0.001
    print("   ✅ Live location message serialization/deserialization works")
    
    # Test 5: ChatMessageResponse
    print("5. Testing ChatMessageResponse...")
    response = messenger_pb2.ChatMessageResponse()
    response.messageSnowflake = 12345
    
    # Add delivery status
    status1 = response.statuses.add()
    status1.user.userId = "user1"
    status1.user.serverId = "server1"
    status1.status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
    
    status2 = response.statuses.add()
    status2.user.userId = "user2"
    status2.user.serverId = "server2"
    status2.status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
    
    serialized = response.SerializeToString()
    deserialized = messenger_pb2.ChatMessageResponse()
    deserialized.ParseFromString(serialized)
    
    assert len(deserialized.statuses) == 2
    assert deserialized.statuses[0].status == messenger_pb2.ChatMessageResponse.Status.DELIVERED
    assert deserialized.statuses[1].status == messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
    print("   ✅ ChatMessageResponse serialization/deserialization works")
    
    # Test 6: Recipient type detection
    print("6. Testing recipient type detection...")
    user_msg = messenger_pb2.ChatMessage()
    user_msg.user.userId = "test"
    assert user_msg.WhichOneof('recipient') == 'user'
    
    group_msg = messenger_pb2.ChatMessage()
    group_msg.group.groupId = "test"
    assert group_msg.WhichOneof('recipient') == 'group'
    
    uog_msg = messenger_pb2.ChatMessage()
    uog_msg.userOfGroup.user.userId = "test"
    assert uog_msg.WhichOneof('recipient') == 'userOfGroup'
    print("   ✅ Recipient type detection works")
    
    # Test 7: Content type detection
    print("7. Testing content type detection...")
    text_msg = messenger_pb2.ChatMessage()
    text_msg.textContent = "test"
    assert text_msg.WhichOneof('content') == 'textContent'
    
    loc_msg = messenger_pb2.ChatMessage()
    loc_msg.live_location.user.userId = "test"
    assert loc_msg.WhichOneof('content') == 'live_location'
    print("   ✅ Content type detection works")
    
    print("\n=== All Protobuf Validations Passed! ===")
    print("✅ ChatMessage structure is correctly implemented")
    print("✅ ChatMessageResponse structure is correctly implemented")
    print("✅ All recipient types (User, Group, UserOfGroup) work")
    print("✅ All content types (text, live_location) work")
    print("✅ Serialization/deserialization works correctly")

if __name__ == "__main__":
    try:
        validate_protobuf_structures()
    except Exception as e:
        print(f"❌ Validation failed: {e}")
        exit(1)
