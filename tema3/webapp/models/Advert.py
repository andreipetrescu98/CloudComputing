
class Advert:

    def __init__(self, id=None, user_id=None, title=None, image=None, description=None, date=None, duration=None, location=None, price=None, availability=None):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.image = image
        self.description = description
        self.date = date
        self.duration = duration
        self.location = location
        self.price = price
        self.availability = availability

    @staticmethod
    def from_dict(source):
        return Advert(source['id'], source['user_id'], source['title'], source['image'], source['description'], source['date'], source['duration'], source['location'], source['price'], source['availability'])

    def to_dict(self):
        advert_dict = {
            u'title': self.title,
            u'user_id': self.user_id,
            u'image': self.image,
            u'description': self.description,
            u'date': self.date,
            u'duration': self.duration,
            u'location': self.location,
            u'price': self.price,
            u'availability': self.availability
        }
        return advert_dict

    def __repr__(self):
        return f"Advert({self.id}, {self.user_id}, {self.title}, {self.image}, {self.description}, {self.date}, {self.duration}, {self.location}, {self.price}, {self.availability})"
