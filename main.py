from client.main import run_client_logic
from GUI.chatwindow import ChatWindow
from PyQt5.QtWidgets import QApplication
import sys
import time
import os

def main():
    # Get user configuration from environment variables
    user_id = os.getenv('CHAT_USER_ID', 'main_client_user')
    recipient_id = os.getenv('CHAT_RECIPIENT_ID', 'other_user')
    
    print(f"Starting GUI for user: {user_id}, default recipient: {recipient_id}")
    
    typing_feature, location_feature, chat_feature = run_client_logic(user_id=user_id)
    
    time.sleep(1)  # doesn't work without this delay, probably due to threading issues
    
    app = QApplication(sys.argv)
    window = ChatWindow(typing_feature, location_feature, chat_feature, default_recipient=recipient_id)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
