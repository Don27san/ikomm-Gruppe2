
from utils import green, red, serialize_msg, parse_msg, live_location
from .feature_base import FeatureBase
from pathlib import Path
from protobuf import messenger_pb2


class DocumentFeature(FeatureBase):
    """
    Handles document-related communication between the client and the server.

    This feature enables requesting documents from the server and receiving them.
    If a document is available, it will be saved to the local `downloads` directory.

    Methods
    __init__():
        Initializes the DocumentFeature based on the FeatureBase.
    trigger_document_download(documentSnowflake: int):
        Sends a request to the server to download a document with the specified identifier.
    handle_message_for_feature(message_name=None, payload=None, conn=None, addr=None):
        Processes incoming messages specific to the document feature and saves documents if available.
    """

    def __init__(self):
        """
        Initializes the DocumentFeature with the feature name 'documents'.
        """
        super().__init__('documents')

    def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
        """
        This method is overwritten from the parent class to handle document specific messages.

        Args:
            message_name (str, optional): The name of the message type received.
            payload (dict, optional): The message payload containing document data.
            conn (socket, optional): The connection object (not used in this handler).
            addr (tuple, optional): The address of the sender (not used in this handler).

        Returns:
            bool: True if the message was handled by this feature, False otherwise.

        Behavior:
            - If the message is 'DOWNLOADING_DOCUMENT' and the result is 'AVAILABLE',
              saves the document to the `downloads` directory.
            - If the document is unavailable or an error occurs, logs an error message.
        """

        if message_name == 'DOWNLOADING_DOCUMENT':
            try:
                if payload['result'] == 'AVAILABLE':
                    filename = str(payload['documentSnowflake'])
                    folder_path = Path("downloads")
                    folder_path.mkdir(parents=True, exist_ok=True)
                    with open(folder_path / filename, 'wb') as f:
                        f.write(payload['data'])
                        green(f"{self.feature_name}: Document {filename} from {self.feature_ip}:{self.feature_port} saved successfully.")
                else:
                    status_name = payload['result']
                    red(f"{self.feature_name}: Download Error. Status: {status_name}.\n")
            except Exception as e:
                red(f"{self.feature_name}: Unknown Error during document download: {e}.\n")

            return True

        else:
            return False

    def trigger_document_download(self, documentSnowflake: int):
        """
        Sends a document download request to the server, triggered in the GUI.

        Args:
            documentSnowflake (int): The unique identifier of the document to be downloaded.

        Behavior:
            - Checks if there is an active connection to the server.
            - Constructs and sends a 'DOWNLOAD_DOCUMENT' request.
            - Logs the request status.
        """
        try:
            if not self.is_connected():
                red(f"\n{self.feature_name}: No connection to server.\n")
                return

            download_msg = messenger_pb2.DownloadDocument()
            download_msg.documentSnowflake = documentSnowflake
            self.client.send_msg((serialize_msg('DOWNLOAD_DOCUMENT', download_msg)))
            green(f"{self.feature_name}: Document {documentSnowflake} requested from {self.feature_ip}:{self.feature_port}.\n")
        except Exception as e:
            red(f"{self.feature_name}: Unknown Error during document request: {e}.\n")
