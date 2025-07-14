
from utils import green, red, serialize_msg, parse_msg, live_location
from .feature_base import FeatureBase
from pathlib import Path
from protobuf import messenger_pb2


class DocumentFeature(FeatureBase):
    """
    ...
    """

    def __init__(self):
        super().__init__('DOCUMENT')

    def handle_message_for_feature(self, message_name=None, payload=None, conn=None, addr=None):
        """
        Handles feature specific message "DownloadingDocument"
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
        Request document download from server
        """
        if not self.is_connected():
            red("Not connected to document server.")
            return
            
        download_msg = messenger_pb2.DownloadDocument()
        download_msg.documentSnowflake = documentSnowflake
        self.client.send_msg((serialize_msg('DOWNLOAD_DOCUMENT', download_msg)))
        green(f"{self.feature_name}: Document {documentSnowflake} requested from {self.feature_ip}:{self.feature_port}.\n")
