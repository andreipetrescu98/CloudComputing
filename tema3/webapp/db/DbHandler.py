from google.cloud import firestore
from webapp.singleton.singleton import Singleton
from webapp.models.Advert import Advert


class DbHandler(metaclass=Singleton):

    def __init__(self, user):
        self.db = firestore.Client()
        self.user = user

    def add_user(self):
        user_document = self.db.collection('users').document(self.user.id).set(self.user.to_dict())

    def get_user_by_id(self):
        user_document_ref = self.db.collection('users').document(self.user.id)
        return user_document_ref.get().to_dict()

    def get_adverts(self):
        adverts = []
        try:
            adverts_ref = self.db.collection('adverts')
            results = adverts_ref.get()

            for item in results:
                adv = Advert(**item.to_dict())
                adv.id = item.id

                adverts.append(adv)
        except Exception as e:
            print(e)

        return adverts

    def get_advert_by_id(self, advert_id):
        adverts_ref = self.db.collection('adverts')
        advert_dict = adverts_ref.document(advert_id).get().to_dict()
        return Advert(**advert_dict)

    def add_advert(self, new_advert):
        new_advert_document_ref = self.db.collection('adverts').document()
        new_advert_document_ref.set(new_advert.to_dict())
        new_advert.id = new_advert_document_ref.id

    def delete_advert(self, advert):
        advert_doc_ref = self.db.collection('adverts').document(advert.id)
        advert_doc_ref.delete()

    def edit_advert(self, advert):
        advert_doc_ref = self.db.collection('adverts').document(advert.id)
        advert_doc_ref.update(advert.to_dict())
