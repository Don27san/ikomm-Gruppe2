\
import socket
import threading
import time
from protobuf import messenger_pb2 # Assuming your compiled protobuf file is here

# Server configuration
HOST = '0.0.0.0' # Listen on all available interfaces
PORT = 6001 # Port for TCP chat service
MAX_CLIENTS = 10
SERVER_ID = "homeserver1" # This server's unique ID

# In-memory storage for connected clients and server/group info (for a real app, use a database)
connected_clients = {} # { (user_id, server_id): client_socket }
# server_directory = { "server_id": ("host", port) } # For inter-server communication
# group_members = { ("group_id", "group_server_id"): [("user_id", "user_server_id")] }

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    client_id_str = f"{addr[0]}:{addr[1]}" # Temporary ID until proper client registration

    try:
        while True:
            # Simple framing: read length of message first, then message
            msg_len_bytes = client_socket.recv(4)
            if not msg_len_bytes:
                print(f"[DISCONNECTED] {addr} (no length bytes received).")
                break
            
            msg_len = int.from_bytes(msg_len_bytes, 'big')
            if msg_len == 0:
                print(f"[DISCONNECTED] {addr} (zero length message).")
                break

            serialized_msg = b''
            while len(serialized_msg) < msg_len:
                chunk = client_socket.recv(msg_len - len(serialized_msg))
                if not chunk:
                    print(f"[DISCONNECTED] {addr} (incomplete message).")
                    return # Exit thread for this client
                serialized_msg += chunk
            
            chat_msg = messenger_pb2.ChatMessage()
            chat_msg.ParseFromString(serialized_msg)

            print(f"[RECEIVED from {addr}] Author: {chat_msg.author.userId}@{chat_msg.author.serverId}")
            print(f"  Content: {chat_msg.textContent}")

            process_chat_message(chat_msg, client_socket, addr)

    except ConnectionResetError:
        print(f"[DISCONNECTED] {addr} (connection reset).")
    except Exception as e:
        print(f"[ERROR] For {addr}: {e}")
    finally:
        # Clean up client connection
        # if client_id_str in connected_clients: # More robust cleanup needed if using user_id based keys
        #     del connected_clients[client_id_str]
        client_socket.close()
        print(f"[CLOSED] Connection with {addr}.")

def process_chat_message(chat_msg, source_socket, source_addr):
    # This server's ID
    current_server_id = SERVER_ID 

    author = chat_msg.author
    recipient_type = chat_msg.WhichOneof('recipient')
    content_type = chat_msg.WhichOneof('content') # e.g. 'textContent'

    # Rule 1: Source is a different server (inter-server message)
    # This basic example doesn't fully implement inter-server connections yet.
    # We assume for now messages are from clients connected directly to this server.
    # If chat_msg.author.serverId != current_server_id: # This would be a message relayed from another server
        # print(f"  Message from another server {chat_msg.author.serverId}")
        # if recipient_type == 'userOfGroup':
        #     if chat_msg.recipient.userOfGroup.group.serverId != current_server_id and \ 
        #        author.serverId != chat_msg.recipient.userOfGroup.group.serverId: # Simplified check
        #         print(f"  Validation Error: Group {chat_msg.recipient.userOfGroup.group.groupId} or author {author.userId} not on source server {author.serverId}")
        #         return # Or send error back
        # elif author.serverId != current_server_id: # Simplified check for direct user/group messages from other servers
        #     pass # Basic validation, more needed

    if recipient_type == 'user':
        target_user = chat_msg.recipient.user
        print(f"  Recipient: User {target_user.userId}@{target_user.serverId}")
        if target_user.serverId == current_server_id:
            # Recipient is on this server, relay to client_id (if known and connected)
            print(f"  Action: Relay to local user {target_user.userId}")
            # relay_to_local_client(target_user.userId, chat_msg)
        else:
            # Recipient is on another server, relay according to server_id
            print(f"  Action: Relay to server {target_user.serverId} for user {target_user.userId}")
            # relay_to_other_server(target_user.serverId, chat_msg)

    elif recipient_type == 'group':
        target_group = chat_msg.recipient.group
        print(f"  Recipient: Group {target_group.groupId}@{target_group.serverId}")
        if target_group.serverId == current_server_id:
            # Recipient group is hosted here. Split into UserOfGroup messages.
            print(f"  Action: Group {target_group.groupId} is local. Splitting message.")
            # members = get_group_members(target_group.groupId, target_group.serverId)
            # for member_user_id, member_server_id in members:
            #     uog_msg = messenger_pb2.ChatMessage()
            #     uog_msg.CopyFrom(chat_msg) # Copy original message details
            #     uog_msg.recipient.userOfGroup.user.userId = member_user_id
            #     uog_msg.recipient.userOfGroup.user.serverId = member_server_id
            #     uog_msg.recipient.userOfGroup.group.groupId = target_group.groupId
            #     uog_msg.recipient.userOfGroup.group.serverId = target_group.serverId
            #     print(f"    Relaying to UserOfGroup: {member_user_id} in {target_group.groupId}")
            #     process_chat_message(uog_msg, None, None) # Recursive call for UserOfGroup
        else:
            # Recipient group is elsewhere, relay to that server
            print(f"  Action: Relay to server {target_group.serverId} for group {target_group.groupId}")
            # relay_to_other_server(target_group.serverId, chat_msg)

    elif recipient_type == 'userOfGroup':
        target_uog = chat_msg.recipient.userOfGroup
        print(f"  Recipient: UserOfGroup {target_uog.user.userId} in {target_uog.group.groupId}@{target_uog.group.serverId}")
        if target_uog.group.serverId == current_server_id:
            # User is part of a group hosted on this server. Relay to specific client.
            print(f"  Action: Relay to local user {target_uog.user.userId} (member of {target_uog.group.groupId})")
            # relay_to_local_client(target_uog.user.userId, chat_msg)
        else:
            # UserOfGroup for a group on another server. This is an error according to rules.
            print(f"  Error: Recipient UserOfGroup for group {target_uog.group.groupId} on another server {target_uog.group.serverId}. This should not happen if source is client.")
            # Potentially send an error message back to the sender if it was a server relaying.

    else:
        print(f"  Unknown recipient type: {recipient_type}")

# Placeholder functions for relaying (these would need actual implementation)
# def relay_to_local_client(user_id, chat_msg):
#     # Find client_socket for user_id and send the message
#     # This requires a mapping of user_id to client_socket upon connection/authentication
#     print(f"    Attempting to relay to local client {user_id}")
#     pass

# def relay_to_other_server(server_id, chat_msg):
#     # Find connection to other server and send the message
#     print(f"    Attempting to relay to other server {server_id}")
#     pass

# def get_group_members(group_id, group_server_id):
#     # Lookup group members from a database or in-memory store
#     print(f"    Looking up members for group {group_id}@{group_server_id}")
#     return [("userA", "homeserver1"), ("userB", "otherserver2")] # Example members

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(MAX_CLIENTS)
    print(f"[LISTENING] Chat server listening on {HOST}:{PORT} with SERVER_ID: {SERVER_ID}")

    try:
        while True:
            client_socket, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(client_socket, addr))
            thread.daemon = True # Daemonize threads
            thread.start()
    except KeyboardInterrupt:
        print("[SHUTTING DOWN] Server is shutting down.")
    finally:
        server.close()

if __name__ == '__main__':
    # Compile protobuf if messenger_pb2.py is outdated or missing
    # This is a simple check; a build script or makefile is better for complex projects.
    # try:
    #     from protobuf import messenger_pb2
    # except ImportError:
    #     print("messenger_pb2.py not found. Attempting to compile...")
    #     import os
    #     # Assuming protoc is in PATH and .proto file is in ../protobuf/
    #     # Adjust path to protoc and .proto file as necessary.
    #     # This is a simplified command.
    #     # You might need to specify python_out path more directly.
    #     # The `.` for proto_path assumes CWD is where `protobuf` dir is a child.
    #     # This might not be robust if script is run from elsewhere.
    #     # Best to run from project root or have clear paths.
    #     # Example: running from ikomm-Gruppe2 directory
    #     # protoc -I=./protobuf --python_out=./protobuf ./protobuf/messenger.proto
    #     # For this script, assuming it's in server/ and protobuf/ is sibling of server/
    #     # This relative path might be tricky.
    #     # A more robust way is to ensure PYTHONPATH includes the project root.
    #     proto_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'protobuf'))
    #     if not os.path.exists(os.path.join(proto_dir, 'messenger_pb2.py')):
    #         print(f"Attempting to compile .proto in {proto_dir}")
    #         # This command assumes protoc is in path and CWD is project root
    #         # For this script, it's better to ensure it's run from project root
    #         # or use absolute paths for protoc command if possible.
    #         # This is a common source of issues.
    #         # A simple os.system call might not have the right CWD or PATH.
    #         # Consider using subprocess module for better control.
    #         # For now, we assume it's compiled.
    #         print("Please ensure messenger.proto is compiled to messenger_pb2.py")
    #         # import subprocess
    #         # subprocess.run(['protoc', f'-I={proto_dir}', f'--python_out={proto_dir}', os.path.join(proto_dir, 'messenger.proto')], check=True)
    #         # print("Compilation successful.")
    #         # # Need to re-import after compilation
    #         # import importlib
    #         # import sys
    #         # # Ensure the protobuf directory is in the path for the import
    #         # if proto_dir not in sys.path:
    #         #     sys.path.insert(0, os.path.abspath(os.path.join(proto_dir, '..')))
    #         # messenger_pb2 = importlib.import_module('protobuf.messenger_pb2')
    #         # print("Re-imported messenger_pb2.py")

    start_server()
