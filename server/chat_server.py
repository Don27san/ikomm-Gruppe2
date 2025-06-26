\
import socket
import threading
import time
from protobuf import messenger_pb2
from config import config

# Server configuration
HOST = '0.0.0.0'  # Listen on all available interfaces
PORT = config['chat_feature']['server_port']  # Port for TCP chat service
MAX_CLIENTS = 10
SERVER_ID = "homeserver1"  # This server's unique ID

# In-memory storage for connected clients and server/group info (for a real app, use a database)
connected_clients = {}  # { user_id: client_socket }
server_directory = {}  # { "server_id": ("host", port) } For inter-server communication
group_members = {}  # { ("group_id", "group_server_id"): [("user_id", "user_server_id")] }

def handle_client(client_socket, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    user_id = None  # Will be set when client registers

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
                    return
                serialized_msg += chunk
            
            chat_msg = messenger_pb2.ChatMessage()
            chat_msg.ParseFromString(serialized_msg)

            print(f"[RECEIVED from {addr}] Author: {chat_msg.author.userId}@{chat_msg.author.serverId}")
            print(f"  Message Snowflake: {chat_msg.messageSnowflake}")
            
            # Register client if not already registered
            if user_id is None:
                user_id = chat_msg.author.userId
                connected_clients[user_id] = client_socket
                print(f"[REGISTERED] Client {user_id} registered")

            response = process_chat_message(chat_msg, client_socket, addr)
            if response:
                send_response(client_socket, response)

    except ConnectionResetError:
        print(f"[DISCONNECTED] {addr} (connection reset).")
    except Exception as e:
        print(f"[ERROR] For {addr}: {e}")
    finally:
        # Clean up client connection
        if user_id and user_id in connected_clients:
            del connected_clients[user_id]
        client_socket.close()
        print(f"[CLOSED] Connection with {addr}.")

def process_chat_message(chat_msg, source_socket, source_addr):
    """
    Process incoming chat message according to the protocol:
    - If source is different server, validate author/group belongs to that server
    - Route message based on recipient type
    - Return ChatMessageResponse
    """
    current_server_id = SERVER_ID
    author = chat_msg.author
    recipient_type = chat_msg.WhichOneof('recipient')
    content_type = chat_msg.WhichOneof('content')

    print(f"  Content type: {content_type}")
    if content_type == 'textContent':
        print(f"  Text content: {chat_msg.textContent}")
    elif content_type == 'live_location':
        print(f"  Live location from: {chat_msg.live_location.user.userId}")

    # Create response message
    response = messenger_pb2.ChatMessageResponse()
    response.messageSnowflake = chat_msg.messageSnowflake

    if recipient_type == 'user':
        target_user = chat_msg.user
        print(f"  Recipient: User {target_user.userId}@{target_user.serverId}")
        
        status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
        if target_user.serverId == current_server_id:
            # Recipient is on this server
            if target_user.userId in connected_clients:
                print(f"  Action: Relay to local user {target_user.userId}")
                relay_to_local_client(target_user.userId, chat_msg)
            else:
                print(f"  User {target_user.userId} not found on this server")
                status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
        else:
            # Recipient is on another server
            print(f"  Action: Relay to server {target_user.serverId}")
            success = relay_to_other_server(target_user.serverId, chat_msg)
            if not success:
                status = messenger_pb2.ChatMessageResponse.Status.OTHER_SERVER_NOT_FOUND

        # Add delivery status
        delivery_status = response.statuses.add()
        delivery_status.user.CopyFrom(target_user)
        delivery_status.status = status

    elif recipient_type == 'group':
        target_group = chat_msg.group
        print(f"  Recipient: Group {target_group.groupId}@{target_group.serverId}")
        
        if target_group.serverId == current_server_id:
            # Group is hosted here - split into UserOfGroup messages
            print(f"  Action: Group {target_group.groupId} is local. Splitting message.")
            members = get_group_members(target_group.groupId, target_group.serverId)
            
            for member_user_id, member_server_id in members:
                # Create UserOfGroup message
                uog_msg = messenger_pb2.ChatMessage()
                uog_msg.CopyFrom(chat_msg)
                # Clear the group recipient and set userOfGroup
                uog_msg.ClearField('group')
                uog_msg.userOfGroup.user.userId = member_user_id
                uog_msg.userOfGroup.user.serverId = member_server_id
                uog_msg.userOfGroup.group.CopyFrom(target_group)
                
                print(f"    Relaying to UserOfGroup: {member_user_id}@{member_server_id}")
                member_response = process_chat_message(uog_msg, None, None)
                if member_response:
                    # Merge member responses into main response
                    for status in member_response.statuses:
                        response.statuses.append(status)
        else:
            # Group is on another server
            print(f"  Action: Relay to server {target_group.serverId}")
            success = relay_to_other_server(target_group.serverId, chat_msg)
            status = messenger_pb2.ChatMessageResponse.Status.DELIVERED if success else messenger_pb2.ChatMessageResponse.Status.OTHER_SERVER_NOT_FOUND
            
            # Add status for the group (represented by a placeholder user)
            delivery_status = response.statuses.add()
            delivery_status.user.userId = f"group_{target_group.groupId}"
            delivery_status.user.serverId = target_group.serverId
            delivery_status.status = status

    elif recipient_type == 'userOfGroup':
        target_uog = chat_msg.userOfGroup
        print(f"  Recipient: UserOfGroup {target_uog.user.userId}@{target_uog.user.serverId} in {target_uog.group.groupId}@{target_uog.group.serverId}")
        
        if target_uog.group.serverId == current_server_id:
            # User is part of a group hosted on this server
            if target_uog.user.userId in connected_clients:
                print(f"  Action: Relay to local user {target_uog.user.userId}")
                relay_to_local_client(target_uog.user.userId, chat_msg)
                status = messenger_pb2.ChatMessageResponse.Status.DELIVERED
            else:
                print(f"  User {target_uog.user.userId} not found")
                status = messenger_pb2.ChatMessageResponse.Status.USER_NOT_FOUND
                
            delivery_status = response.statuses.add()
            delivery_status.user.CopyFrom(target_uog.user)
            delivery_status.status = status
        else:
            # UserOfGroup for a group on another server - this is an error
            print(f"  Error: UserOfGroup for group on another server {target_uog.group.serverId}")
            delivery_status = response.statuses.add()
            delivery_status.user.CopyFrom(target_uog.user)
            delivery_status.status = messenger_pb2.ChatMessageResponse.Status.OTHER_ERROR

    else:
        print(f"  Unknown recipient type: {recipient_type}")
        # Add error status
        delivery_status = response.statuses.add()
        delivery_status.user.CopyFrom(author)  # Return error to sender
        delivery_status.status = messenger_pb2.ChatMessageResponse.Status.OTHER_ERROR

    return response


def relay_to_local_client(user_id, chat_msg):
    """Relay message to a local client"""
    if user_id in connected_clients:
        try:
            client_socket = connected_clients[user_id]
            serialized_msg = chat_msg.SerializeToString()
            msg_len = len(serialized_msg).to_bytes(4, 'big')
            client_socket.sendall(msg_len + serialized_msg)
            print(f"    Successfully relayed to local client {user_id}")
            return True
        except Exception as e:
            print(f"    Error relaying to local client {user_id}: {e}")
            # Remove disconnected client
            del connected_clients[user_id]
            return False
    else:
        print(f"    Client {user_id} not connected")
        return False


def relay_to_other_server(server_id, chat_msg):
    """Relay message to another server"""
    if server_id in server_directory:
        try:
            host, port = server_directory[server_id]
            # TODO: Implement inter-server communication
            print(f"    Would relay to server {server_id} at {host}:{port}")
            return True  # Placeholder
        except Exception as e:
            print(f"    Error relaying to server {server_id}: {e}")
            return False
    else:
        print(f"    Server {server_id} not found in directory")
        return False


def get_group_members(group_id, group_server_id):
    """Get members of a group"""
    group_key = (group_id, group_server_id)
    if group_key in group_members:
        return group_members[group_key]
    else:
        # Return some example members for testing
        print(f"    Group {group_id} not found, returning example members")
        return [("user1", SERVER_ID), ("user2", SERVER_ID)]


def send_response(client_socket, response):
    """Send ChatMessageResponse back to client"""
    try:
        serialized_response = response.SerializeToString()
        msg_len = len(serialized_response).to_bytes(4, 'big')
        client_socket.sendall(msg_len + serialized_response)
        print(f"  Sent response with {len(response.statuses)} delivery statuses")
    except Exception as e:
        print(f"  Error sending response: {e}")

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
