from gcloud import storage
import os
import pickle
from google.oauth2.credentials import Credentials

storage_client = storage.Client.from_service_account_json('config\storage_credentials.json')

bucket = storage_client.get_bucket('cloudcomputing-272912.appspot.com')

# def upload_advert_image(advert):
#     blob = bucket.blob(f'adverts/{advert.id}.jpg')
#     blob.upload_from_filename(filename=f"{advert.id}.jpg")

# def download_advert_image(advert):
#     blob = bucket.get_blob(f'adverts/{advert.id}.jpg')
#     print(blob.name)
#     with open(f'{advert.id}.jpg', 'wb') as f:
#         f.write(blob.download_as_string())

def upload_advert_image(advert):
    blob = bucket.blob(r'adverts/{advert.id}.jpg')
    blob.upload_from_filename(filename="dog.jpg")
    blob.make_public()
    return blob.public_url

def download_advert_image(advert):
    blob = bucket.get_blob(r'adverts/{advert.id}.jpg')
    return blob.public_url
    # with open('dog-test.jpg', 'wb') as f:
    #     f.write(blob.download_as_string())

# upload_advert_image(None)
# download_advert_image(None)