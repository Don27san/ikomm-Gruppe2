from .feature_base import FeatureBase
from typing import Literal
from protobuf import messenger_pb2
from utils import generate_chat_message
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
        print("Trying to send translation")
        """
        Sends a translation request to the server of group 4.
        
        Args:
            text (str): The text to be translated.
            target_language (str): The language to translate the text into.
        """
        if not self.is_connected():
            red("Not connected to translation server.")
            return
            
        # It would be best to use send_message function from chat_feature.py
        
        # Construct the translation request message

        translation = messenger_pb2.Translate()
        translation.target_language=target_language
        translation.original_text=text


        # msg = generate_chat_message(
        #     author_user_id="user123",
        #     author_server_id="server456", 
        #     recipient={
        #         "user": {
        #             "userId": recipient_user_id, 
        #             "serverId": recipient_server_id,
        #         }
        #     },
        #     content={
        #         "translation": messenger_pb2.Translation(
        #             original_message=text,
        #             target_language=target_language
        #         )
        #     }
        # )

        print(translation)

        self.client.send_msg(serialize_msg("TRANSLATE", translation))

        def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
            if message_name == "TRANSLATE":
                print(payload)
                self.chat_feature.send_message()
        

        