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
       


    def send_translation_request(self, text : str, target_language: target_languages):
        """
        Sends a translation request to the server of group 4.
        
        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into.
        """
      
        # Construct the translation request message
        msg = generate_chat_message(
            author_user_id="user123",
            author_server_id="server456", 
            recipient={
                "user": {
                    "userId": "user789", #Todo @Chang: Needs to be replaced with data from UI 
                    "serverId": "server456" #Todo @Chang: Needs to be replaced with data from UI 
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