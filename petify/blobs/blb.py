from azure.storage.blob import BlobServiceClient

from singleton.singleton import Singleton
from keyvault.akv import get_storage_secret

import base64

class BlobStorage(metaclass=Singleton):
    def __init__(self):
        account_key = get_storage_secret()
        connection_string = 'DefaultEndpointsProtocol=https;AccountName=petifystorage;AccountKey=OV2TrJRp6qOu1bLn+r18Y4qY2oBaDH/RfsDVcieZbS7KedWZET6txQY1Er/KuqmZBkVNd78zdqSGkOp+rn+3Yg==;EndpointSuffix=core.windows.net'
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        self.container_name = 'petifyblob'

    def upload(self, advert_id, image_data: str):
        imgdata = base64.b64decode(image_data)
        blob_client = self.blob_service_client.get_blob_client(container=self.container_name, blob=advert_id + '.png')
        blob_client.upload_blob(imgdata)

