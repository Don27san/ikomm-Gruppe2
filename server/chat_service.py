from .service_base import ServiceBase, FeatureName
from config import config
from utils import serialize_msg, red, green, yellow
from protobuf import messenger_pb2

class ChatService(ServiceBase):
    def __init__(self):
        super().__init__('CHAT_MESSAGE', bind_port=config['chat_feature']['server_connection_port'])
        self.message_history = {} # Using dict to store messages with snowflake as key

    def handle_connections(self):
        # Overriding to remove forwarding logic, as chat is TCP based and handled differently
        super().handle_connections()

    def handle_feature_message(self, message_name, data, conn, addr):
        if message_name == 'CHAT_MESSAGE':
            subscriberIP = addr[0]
            author_info = data.get('author', {})
            user_id = author_info.get('userId', 'Unknown')
            server_id = author_info.get('serverId', 'Unknown')
            message_text = data.get('textContent', '')
            green(f"Received CHAT_MESSAGE from @{user_id}@{server_id} ({subscriberIP}): \"{message_text}\"")

            # Create a ChatMessage protobuf object from the dictionary
            chat_message = messenger_pb2.ChatMessage()
            chat_message.messageSnowflake = int(data['messageSnowflake'])
            if 'author' in data:
                chat_message.author.userId = data['author'].get('userId', '')
                chat_message.author.serverId = data['author'].get('serverId', '')
            
            # Reconstruct the recipient from the data dictionary
            if 'user' in data:
                chat_message.user.userId = data['user'].get('userId', '')
                chat_message.user.serverId = data['user'].get('serverId', '')
            elif 'group' in data:
                # Handle group recipient if necessary
                pass

            if 'textContent' in data:
                chat_message.textContent = data['textContent']
            # TODO: Handle other parts of the message like recipient, document, etc.

            self.message_history[chat_message.messageSnowflake] = chat_message

            self.route_message(chat_message)
            return True # Explicitly signal that the message was handled
        
        elif message_name == 'MESSAGE_ACK':
            green(f"Received ACK for message {data.get('messageSnowflake')} from {addr[0]}")
            
            # Find original message to know who the author was
            original_message = self.message_history.get(int(data.get('messageSnowflake')))
            if not original_message:
                yellow(f"Could not find original message for ACK with snowflake {data.get('messageSnowflake')}")
                return True

            # Create ACK response and route to author
            ack_response = messenger_pb2.ChatMessageResponse()
            ack_response.messageSnowflake = int(data.get('messageSnowflake'))
            if 'statuses' in data:
                for status_data in data['statuses']:
                    status = ack_response.statuses.add()
                    if 'user' in status_data:
                        status.user.userId = status_data['user'].get('userId', '')
                        status.user.serverId = status_data['user'].get('serverId', '')
                    if 'status' in status_data:
                        status.status = messenger_pb2.ChatMessageResponse.Status.Value(status_data['status'])

            # Route ACK to author using same logic as message routing
            if original_message.author.serverId == config['serverId']:
                # Author is local
                for sub_data in self.subscriber_dict.values():
                    if 'user' in sub_data and sub_data['user']['userId'] == original_message.author.userId:
                        try:
                            sub_data['conn'].sendall(serialize_msg('MESSAGE_ACK', ack_response))
                            green(f"Forwarded ACK to local author {original_message.author.userId}")
                        except Exception as e:
                            red(f"Failed to forward ACK to local author: {e}")
                        return True
                red(f"Local author {original_message.author.userId} not found.")
            else:
                # Author is on another server
                for server_ip, server_data in self.server_dict.items():
                    if server_data.get('serverId') == original_message.author.serverId:
                        conn = server_data['functions'].get('CHAT_MESSAGE', {}).get('conn')
                        if conn:
                            try:
                                conn.sendall(serialize_msg('MESSAGE_ACK', ack_response))
                                green(f"Forwarded ACK to server {original_message.author.serverId}")
                            except Exception as e:
                                red(f"Failed to send ACK to server: {e}")
                                conn.close()
                                server_data['functions']['CHAT_MESSAGE']['conn'] = None
                        else:
                            red(f"No connection to server {original_message.author.serverId}")
                        return True
                red(f"Server {original_message.author.serverId} not found.")
            return True

    def route_message(self, chat_message):
        recipient_type = chat_message.WhichOneof('recipient')

        if recipient_type == 'user':
            recipient_user = chat_message.user
            # Check if the recipient is on this server or another one
            if recipient_user.serverId == config['serverId']:
                self.send_msg_to_user(chat_message)
            else:
                self.send_msg_to_server(chat_message)
        
        elif recipient_type == 'group':
            # TODO: Implement group messaging logic
            # This would involve checking the group's serverId and then either handling locally or forwarding.
            yellow("Group messaging not yet implemented.")

        else:
            yellow("Recipient not specified")

    def send_msg_to_user(self, chat_message):
        serialized_message = serialize_msg('CHAT_MESSAGE', chat_message)
        recipient_user = chat_message.user
        
        # Find the subscriber corresponding to this user on this server
        for data in self.subscriber_dict.values():
            if 'user' in data and data['user']['userId'] == recipient_user.userId:
                try:
                    conn = data['conn']
                    conn.sendall(serialized_message)
                    yellow(f"Forwarded chat message to local user {recipient_user.userId}")
                    return
                except Exception as e:
                    red(f"Failed to send message to local user {recipient_user.userId}: {e}")
                    return

        red(f"Local recipient {recipient_user.userId} not found or not connected.")

    def send_msg_to_server(self, chat_message):
        recipient_user = chat_message.user
        target_server_id = recipient_user.serverId
        yellow(f"Attempting to forward message to server: {target_server_id}")

        # Find the server in the server_dict by its serverId
        for server_ip, server_data in self.server_dict.items():
            if server_data.get('serverId') == target_server_id:
                chat_feature_info = server_data['functions'].get('CHAT_MESSAGE')

                if not chat_feature_info:
                    red(f"CHAT_MESSAGE feature not available for server {target_server_id}")
                    return

                conn = chat_feature_info.get('conn')
                if conn:
                    try:
                        serialized_message = serialize_msg('CHAT_MESSAGE', chat_message)
                        conn.sendall(serialized_message)
                        green(f"Successfully forwarded message to server {target_server_id}")
                    except Exception as e:
                        red(f"Failed to send to {target_server_id} at {server_ip}. Error: {e}")
                        conn.close()
                        chat_feature_info['conn'] = None
                else:
                    red(f"No active connection to server {target_server_id}. Cannot forward message.")
                return

        red(f"Server {target_server_id} not found in server_dict.")

    def stop(self):
        super().stop()
        green("Chat service stopped.")

