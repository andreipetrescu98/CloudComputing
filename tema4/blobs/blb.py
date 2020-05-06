from azure.storage.blob import BlockBlobService, PublicAccess
from singleton.singleton import Singleton
from keyvault.akv import get_storage_secret

# accountname = 'petifystorage'
# accountkey = 'OV2TrJRp6qOu1bLn+r18Y4qY2oBaDH/RfsDVcieZbS7KedWZET6txQY1Er/KuqmZBkVNd78zdqSGkOp+rn+3Yg=='
#
# block_blob_service = BlockBlobService(account_name=accountname, account_key=accountkey)
#
# container_name = 'petifyblob'
# file_path = 'C:\\Users\\Matei\\Documents\\Faculty\\Anul 3\\Semestrul 2\\CC\\Homework3\\CC_Tema3\\dog-test.jpg'
# block_blob_service.create_container(container_name)
#
# # Set the permission so the blobs are public.
# block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)
# file_name = 'userid'
# block_blob_service.create_blob_from_path(container_name=container_name, blob_name=file_name + '.png', file_path=file_path)
import base64



class BlobStorage(metaclass=Singleton):
    def __init__(self, config):
        account_key = get_storage_secret()
        self.block_blob_service = BlockBlobService(account_name=config['account_name'], account_key=account_key)
        self.container_name = 'petifyblob'

    def upload(self, advert_id, image_data: str):
        self.block_blob_service.create_container(self.container_name)
        self.block_blob_service.set_container_acl(self.container_name, public_access=PublicAccess.Container)
        imgdata = base64.b64decode(image_data)
        self.block_blob_service.create_blob_from_bytes(
            container_name=self.container_name,
            blob_name=advert_id + '.png',
            blob=imgdata)
