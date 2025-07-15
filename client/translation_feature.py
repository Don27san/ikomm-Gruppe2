from utils.colors import green
from .feature_base import FeatureBase
from typing import Literal
from protobuf import messenger_pb2
from utils import serialize_msg, red
from .chat_feature import ChatFeature

target_languages = Literal[
    'DE',  # German
    'EN',  # English
    'ZH',  # Chinese
]

class TranslationFeature(FeatureBase):
    
    def __init__(self, chat_feature: ChatFeature):
        super().__init__('TRANSLATION')  #Takes care of connection
        self.chat_feature = chat_feature


    def send_translation_request(self, text : str, target_language: target_languages, recipient_user_id : str, recipient_server_id: str):
        """
        Sends a translation request to the server of group 4 and receives the translated content back.
        
        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into.
        """
        if not self.is_connected():
            red("Feature inactive because  connected to translation server.")
            return
        
            # Store recipient information for later use
        self.recipient_user_id = recipient_user_id
        self.recipient_server_id = recipient_server_id
        
        # Construct the translation request message
        translation = messenger_pb2.Translate()
        translation.target_language=target_language
        translation.original_text=text

        self.client.send_msg(serialize_msg("TRANSLATE", translation))
        green(f"Translation request sent for text '{text}' to '{target_language}' language.")



    def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
        if message_name == "TRANSLATED":
            print(f"Received translation: '{payload['translated_text']}' in '{payload['target_language']}' language.")
            self.chat_feature.send_message(
                self.recipient_user_id,
                self.recipient_server_id,
                content={
                    "textContent": payload['translated_text'],
                }
            )
            green(f"Translated message sent to {self.recipient_user_id}@{self.recipient_server_id}.")

        