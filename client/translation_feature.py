from .feature_base import FeatureBase
from typing import Literal
from protobuf import messenger_pb2
from utils import generate_chat_message
from utils import serialize_msg

target_languages = Literal[
    'DE',  # German
    'EN',  # English
    'ZH',  # Chinese
]

class TranslationFeature(FeatureBase):
    
    def __init__(self):
        super().__init__('Translation')  #Takes care of connection
       


    def send_translation_request(self, text : str, target_language: target_languages, recipient_user_id : str, recipient_server_id: str):
        """
        Sends a translation request to the server of group 4.
        
        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into.
        """
        # It would be best to use send_message function from chat_feature.py
        
        # Construct the translation request message
        msg = generate_chat_message(
            author_user_id="user123",
            author_server_id="server456", 
            recipient={
                "user": {
                    "userId": recipient_user_id, 
                    "serverId": recipient_server_id,
                }
            },
            content={
                "translation": messenger_pb2.Translation(
                    original_message=text,
                    target_language=target_language
                )
            }
        )

        print(msg)

        self.client.send_msg(serialize_msg("TRANSLATE", msg))