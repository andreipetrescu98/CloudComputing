from azure.cosmos.cosmos_client import CosmosClient

from models.Advert import Advert
from singleton.singleton import Singleton
from keyvault.akv import get_db_secret


class DbHandler(metaclass=Singleton):

    database_id = 'petify'
    users_container_id = 'users'
    adverts_container_id = 'ads'
    subscriptions_container_id = 'subscriptions'

    def __init__(self, config):
        auth_dict = get_db_secret()
        self.client = CosmosClient(config['endpoint'], auth_dict)

    def user_already_exists(self, user_doc):
        users_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.users_container_id
        uid = user_doc['user_id']
        res = self.client.QueryItems(users_table_ref,
                                     f'SELECT * FROM {DbHandler.users_container_id} u WHERE u.user_id="{uid}"',
                                     {'enableCrossPartitionQuery': True}, partition_key='/user_id')

        if len(list(res)) > 0:
            user_res = next(iter(res))
            user_res.update(user_doc)
            self.client.ReplaceItem(document_link=user_res['_self'],
                                    new_document=user_res,
                                    options={'enableCrossPartitionQuery': True, 'partition_key': '/user_id'})
            return True

        return False

    def add_user(self, user_doc):
        users_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.users_container_id
        self.client.UpsertItem(users_table_ref, user_doc)

    def get_adverts(self):
        adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
        res = self.client.QueryItems(adverts_table_ref, f"SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.availability = true",
                                     {'enableCrossPartitionQuery': True}, partition_key='/availability')

        all_adverts = list(map(Advert.from_dict, res))

        # Get available adverts
        subscriptions_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.subscriptions_container_id
        res_subs = self.client.QueryItems(subscriptions_table_ref,
                                          f"SELECT * FROM {DbHandler.subscriptions_container_id}",
                                          {'enableCrossPartitionQuery': True}, partition_key='/user_id')
        res_subs_list = list(iter(res_subs))
        subscribed_ads = [item["advert_id"] for item in res_subs_list]
        # Filter
        adverts = list(filter(lambda adv: adv.id not in subscribed_ads, all_adverts))

        return adverts

    def get_advert_by_id(self, advert_id):
        try:
            adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
            res = self.client.QueryItems(adverts_table_ref,
                                         f'SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.id="{advert_id}"',
                                         {'enableCrossPartitionQuery': True}, partition_key='/availability')
            advert_doc = next(iter(res))
            return Advert.from_dict(advert_doc)
        except:
            return None

    def add_advert(self, advert):
        adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
        new_advert = advert.to_dict()
        res = self.client.UpsertItem(adverts_table_ref, new_advert)
        advert.id = res['id']

    def edit_advert(self, advert):
        adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
        res = self.client.QueryItems(adverts_table_ref,
                                     f'SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.id="{advert.id}"',
                                     {'enableCrossPartitionQuery': True}, partition_key='/availability')
        advert_doc = next(iter(res))
        advert_doc.update(advert.to_dict())
        print(advert_doc['_self'])
        self.client.ReplaceItem(document_link=advert_doc['_self'], new_document=advert_doc,
                                options={'enableCrossPartitionQuery': True, 'partition_key': '/availability'})

    def get_user_adverts(self, user_id):
        adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
        res = self.client.QueryItems(adverts_table_ref,
                                     f"SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.user_id = '{user_id}'",
                                     {'enableCrossPartitionQuery': True}, partition_key='/user_id')

        return list(map(Advert.from_dict, res))

    def subscribe_user_to_advert(self, user_id, advert_id):
        subscriptions_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.subscriptions_container_id
        item = {"user_id": user_id, "advert_id": advert_id}
        self.client.UpsertItem(subscriptions_table_ref, item)

    def get_user_subscriptions(self, user_id):
        subscriptions_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.subscriptions_container_id
        res = self.client.QueryItems(subscriptions_table_ref,
                                     f"SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.user_id = '{user_id}'",
                                     {'enableCrossPartitionQuery': True}, partition_key='/user_id')

        subs_ids = list(iter(res))
        subscribed_ads = [item["advert_id"] for item in subs_ids]
        # Filter ads by subscriptions
        adverts_table_ref = "dbs/" + DbHandler.database_id + "/colls/" + DbHandler.adverts_container_id
        res = self.client.QueryItems(adverts_table_ref, f"SELECT * FROM {DbHandler.adverts_container_id} a WHERE a.availability = true",
                                     {'enableCrossPartitionQuery': True}, partition_key='/availability')

        subscriptions = list(filter(lambda adv: adv.id in subscribed_ads, list(map(Advert.from_dict, res))))

        return subscriptions


if __name__ == '__main__':
    import json
    import os

    db_credentials = json.load(open(os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                                 'configs/db_credentials.json')))
    db = DbHandler(db_credentials)

    # print(db.get_user_adverts("carbunebogdan@gmail.com"))
    # print(db.get_adverts())
    # db.subscribe_user_to_advert("carbunebogdan@gmail.com", '05ba9979-5a15-4e17-b88b-192421300a01')

    # print(db.get_user_subscriptions("carbunebogdan@gmail.com"))

    user1 = {
    "access_token": "ya29.a0Ae4lvC2UjptJwOkFGDmbXaGkjzrdPbEYbcsCqJ5o6vfSB2wneQ_tk-PxZAYvOPTBYBaK55vKyHbQrjcMrsyMP8z98E6V_1LGNboRZFOxVVlyrsBe6dgE5CkAgxEjatXficqi4iAOQAxR_wvyNgjDLvkXnCWNhhwXsJcrDIPzTudE",
    "expires_on": "2020-05-25T17:23:25.4757555Z",
    "id_token": "eyJhbGciOiJSUzI1NiIsImtpZCI6IjI4Yjc0MWU4ZGU5ODRhNDcxNTlmMTllNmQ3NzgzZTlkNGZhODEwZGIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIxMDE5MzIzMDU3OTcyLTNsdjExOGRva3FiajBlNzRjczAzanFqZnFkdjA3MXBiLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwiYXVkIjoiMTAxOTMyMzA1Nzk3Mi0zbHYxMThkb2txYmowZTc0Y3MwM2pxamZxZHYwNzFwYi5hcHBzLmdvb2dsZXVzZXJjb250ZW50LmNvbSIsInN1YiI6IjEwNjAyMDcwMjczNjU3NzAwMzY5NiIsImVtYWlsIjoiY2FyYnVuZWJvZ2RhbkBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwiYXRfaGFzaCI6Ikt2R0lFX2FZM3cyT2lGWnV6S1pycWciLCJuYW1lIjoiQ2FyYnVuZSBCb2dkYW4iLCJwaWN0dXJlIjoiaHR0cHM6Ly9saDMuZ29vZ2xldXNlcmNvbnRlbnQuY29tL2EtL0FPaDE0R2laQUZkNUtDZk41aUdDWENEZkgzUjVBT2dFd1F3Z1VzcmVUU2xndnc9czk2LWMiLCJnaXZlbl9uYW1lIjoiQ2FyYnVuZSIsImZhbWlseV9uYW1lIjoiQm9nZGFuIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE1ODc4MzE4MDYsImV4cCI6MTU4NzgzNTQwNn0.Xkeggo1D_zJIiIuM2hUB9bnkMfhY22ALuQMUrjCbS0odb1Er6DNvmcfxmD_ISZGZTmejN5ZNwjfVZxroeTyabW8KiLVLooUioYsCA8LRT_xfSprocUFlCBhtsZMe6oULQTnQnBIyO-l3DHXOt-PBue5zK95tZGxL_OnkniSEsWMVJgDAXL4mVr6m3TzAkvWp0vLBVhxCaA_Rsp9dZ9dBrwSsOWOLEqHgP-shevyRhPT9nlL5e61q-LSTgUymVMWiGKjEumw-uqBk5xsfBv7zxlbKtWxVn1kmWuCenn34k1TGyNpNrrwouJ32jMmKi5D01hyy3Tg8Kyx1FXtsv3-OdQ",
    "provider_name": "google",
    "user_claims": [
        {
            "typ": "iss",
            "val": "https://accounts.google.com"
        },
        {
            "typ": "azp",
            "val": "1019323057972-3lv118dokqbj0e74cs03jqjfqdv071pb.apps.googleusercontent.com"
        },
        {
            "typ": "aud",
            "val": "1019323057972-3lv118dokqbj0e74cs03jqjfqdv071pb.apps.googleusercontent.com"
        },
        {
            "typ": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/nameidentifier",
            "val": "106020702736577003696"
        },
        {
            "typ": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/emailaddress",
            "val": "carbunebogdan@gmail.com"
        },
        {
            "typ": "email_verified",
            "val": "true"
        },
        {
            "typ": "at_hash",
            "val": "KvGIE_aY3w2OiFZuzKZrqg"
        },
        {
            "typ": "name",
            "val": "Carbune Bogdan"
        },
        {
            "typ": "picture",
            "val": "https://lh3.googleusercontent.com/a-/AOh14GiZAFd5KCfN5iGCXCDfH3R5AOgEwQwgUsreTSlgvw=s96-c"
        },
        {
            "typ": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/givenname",
            "val": "Carbune"
        },
        {
            "typ": "http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname",
            "val": "Bogdan"
        },
        {
            "typ": "locale",
            "val": "en"
        },
        {
            "typ": "iat",
            "val": "1587831806"
        },
        {
            "typ": "exp",
            "val": "1587835406"
        }
    ],
    "user_id": "carbunebogdan@gmail.com",
    "id": "c94d98d4-99ee-4032-b3e9-c5c451821ae7",
    "_rid": "QPx6AL8BfioBAAAAAAAAAA==",
    "_self": "dbs/QPx6AA==/colls/QPx6AL8Bfio=/docs/QPx6AL8BfioBAAAAAAAAAA==/",
    "_etag": "\"0f00448e-0000-0700-0000-5ea469900000\"",
    "_attachments": "attachments/",
    "_ts": 1587833232
}
#     user2 = {'user_id': 'andrei.p2998@gmail.com'}
#     print(db.user_already_exists(user1))
#     print(db.user_already_exists(user2))
#
#     db.add_user(user2)

    from datetime import datetime, timedelta
    from pytz import timezone

    tz_location = 'Europe/Bucharest'
    date_fmt = '%Y-%m-%dT%H:%M:%S'
    tz = timezone(tz_location)
    start_time = datetime.now(tz)
    end_time = start_time + timedelta(minutes=20)

    advert1 = Advert(id=None,
                     title='Plimba ursu, taie-i capu',
                     image='https://petifystorage.blob.core.windows.net/petifyblob/bear.png',
                     description='Plimba ursu, nu taia frunze la caini',
                     start_date=start_time.strftime(date_fmt),
                     end_date=end_time.strftime(date_fmt),
                     location=tz_location,
                     price=20,
                     availability=True,
                     user_id="carbunebogdan@gmail.com",
                     user_name="Carbune Bogdan",
                     user_picture="https://lh3.googleusercontent.com/a-/AOh14GiZAFd5KCfN5iGCXCDfH3R5AOgEwQwgUsreTSlgvw=s96-c"
                     )

    # db.add_advert(advert1)
    # print(advert1.id)

    # print(db.get_adverts())
    #
    # advert = db.get_advert_by_id('3ea9f3ec-7279-43d7-9042-d64b96547748')
    # advert.availability = False
    #
    # db.edit_advert(advert)

    # endpoint = 'https://petifydb.documents.azure.com:443/'
    # masterKey = '4qJr3ZgHEwRnSPC8zwLlngFyV8tmXhITtl6moqYHXGUyLuoYYQjktRtNQRWWrcyo63JBUpr427yN6bnrY2FmOQ=='
    # resourceTokens = '5q9rIzeUeJBLJlLTGmxIPZ4PLegngYHZui4TWFxN1uEuGyd2fstrZqCiUGDECWW94jAgnivWddVT6yXsYxZQRQ=='
    # #
    # client = CosmosClient(url_connection=endpoint, auth={"masterKey": masterKey, "resourceTokens": resourceTokens})

    # database_id = 'petify'
    # users_container_id = 'users'
    # users_table_ref = "dbs/" + database_id + "/colls/" + users_container_id

    # Get users container
    # users_container = client.ReadContainer(users_table_ref)
    #
    # # Get user by id
    # user_id = "c94d98d4-99ee-4032-b3e9-c5c451821ae7"
    # res = client.QueryItems(users_table_ref, f'SELECT * FROM users u WHERE u.id="{user_id}"', {'enableCrossPartitionQuery': True}, partition_key='/user_id')
    # user_doc = next(iter(res))

    # Insert user in container
    # new_user = {"id": None, "username": "New User 2", "email": "new.user.2@example.com", "category": "standard"}
    # item = client.UpsertItem(users_table_ref, new_user)
    # print(item['_self'])

    # Edit user
    # user_doc.update({"username": "Niculaie Paleru"})
    # res = client.ReplaceItem(document_link=user_doc['_self'], new_document=user_doc, options={'enableCrossPartitionQuery': True, 'partition_key': '/category'})

    # Delete user from container
    # user_ref = users_table_ref + "/docs/" + user_id
    # del_res = client.DeleteItem(user_ref, {'enableCrossPartitionQuery': True, 'partitionKey': '/category'})
    # print(del_res)
    # for item in client.QueryItems(users_table_ref, 'SELECT * FROM users u', {'enableCrossPartitionQuery': True}, partition_key='/category'):
    #     print(item)
