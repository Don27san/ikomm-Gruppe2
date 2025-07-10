import socket
import time
import geocoder
import random
import math
from utils import green, red, serialize_msg, parse_msg, live_location
from config import config
from .feature_base import FeatureBase

import queue
import time

from utils import ConnectionHandler, red, yellow, green, blue, parse_msg, serialize_msg, connect_client, ping, pong
from typing import Literal
from config import config
from pathlib import Path

from protobuf import messenger_pb2

# class DocumentFeature(FeatureBase):
#     """
#     ...
#     """
#     super().__init__('DOCUMENT')
#
#     def handle_message_for_feature(self, message_name=None, payload=None):
#         """
#         Updated for each feature individually if it receives messages beyond the _handle_base_messages function
#         """
#
#         if message_name == 'DOWNLOADING_DOCUMENT':
#             self.handle_message()
#             return True
#             if payload['result'] == 'AVAILABLE':
#                 filename = str(payload['documentSnowflake'])
#                 folder_path = Path("downloads")
#                 folder_path.mkdir(parents=True, exist_ok=True)
#                 with open(folder_path / filename, 'wb') as f:
#                     f.write(payload['data'])
#                     print(f"{self.feature_name}: Document {filename} saved successfully.")
#
#
#
#
#             test_msg = messenger_pb2.DownloadingDocument()
#             if test_msg.result == messenger_pb2.DocumentStatus.Result.AVAILABLE:
#                 print()
#
#             return True
#
#         else:
#             return False
#
#     def trigger_document_download(self, documentId):
#         pass
#
# # 4. Warte auf die Antwort und speichere die Datei
#         try:
#             response_event = await asyncio.wait_for(future, timeout=30.0)  # Längerer Timeout für Downloads
#             response = response_event.content
#
#             if response.result == features.documents.DocumentStatus.Result.AVAILABLE:
#                 with open(output_filename, 'wb') as f:
#                     f.write(response.data)
#                 print(f"Dokument {doc_id} erfolgreich heruntergeladen und als '{output_filename}' gespeichert.")
#             else:
#                 # Hole den Statusnamen für die Fehlermeldung
#                 status_name = features.documents.DocumentStatus.Result.Name(response.result)
#                 print(f"Fehler beim Download: Server meldet Status '{status_name}'.")
#
#         except asyncio.TimeoutError:
#             print("Fehler: Zeitüberschreitung beim Download.")
#         except Exception as e:
#             print(f"Ein Fehler ist beim Download aufgetreten: {e}")
#         finally:
#             self.pending_requests.pop(doc_id, None)