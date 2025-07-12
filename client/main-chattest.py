# client/main-chattest.py - Chat function only test

import sys
import threading
import time
from .discovery_service import DiscoveryService
from .chat_feature import ChatFeature
from config import config

def run_chat_test():
    # Override config for user2
    config['user']['userId'] = 'user2'
    config['user']['serverId'] = 'ikomm_gruppe_2'
    
    print(f"Starting chat test as {config['user']['userId']}@{config['user']['serverId']}")
    
    discovery = DiscoveryService()
    server_list = discovery.discover_servers()

    # Only chat feature for testing
    chat_feature = ChatFeature()
    chat_thread = threading.Thread(target=chat_feature.handle_connection, args=(server_list,), daemon=True)
    chat_thread.start()
    
    # Wait a moment for connection to establish
    time.sleep(2)
    
    # Send test messages to user1
    recipient_user = "user1"
    recipient_server = "ikomm_gruppe_2"
    
    test_messages = [
        "Hello user1, this is user2!",
        "Testing chat functionality",
        "How are you doing?",
        "This is a test message from the chat test script"
    ]
    
    print(f"Sending messages to {recipient_user}@{recipient_server}:")
    
    for i, message in enumerate(test_messages, 1):
        print(f"Sending message {i}: {message}")
        chat_feature.send_message(recipient_user, recipient_server, message)
        time.sleep(3)  # Wait 3 seconds between messages
    
    print("Chat test completed. Keeping connection alive...")
    return chat_feature

def main():
    chat_feature = run_chat_test()
    try:
        while True:
            time.sleep(1)  # Keep the program alive
    except KeyboardInterrupt:
        print("\nStopping chat test...")
        chat_feature.stop()

if __name__ == "__main__":
    main()
