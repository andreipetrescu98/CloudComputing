

class Advert:

    def __init__(self, id=None, title=None, image=None, description=None, start_date=None, end_date=None, location=None, price=None, availability=None, user_id=None, user_name=None, user_picture=None):
        self._id = id
        self._title = title
        self._image = image
        self._description = description
        self._start_date = start_date
        self._end_date = end_date
        self._location = location
        self._price = price
        self._availability = availability
        self._user_id = user_id
        self._user_name = user_name
        self._user_picture = user_picture

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def start_date(self):
        return self._start_date

    @start_date.setter
    def start_date(self, value):
        self._start_date = value

    @property
    def end_date(self):
        return self._end_date

    @end_date.setter
    def end_date(self, value):
        self._end_date = value

    @property
    def location(self):
        return self._location

    @location.setter
    def location(self, value):
        self._location = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value

    @property
    def availability(self):
        return self._availability

    @availability.setter
    def availability(self, value):
        self._availability = value

    @property
    def user_id(self):
        return self._user_id

    @user_id.setter
    def user_id(self, value):
        self._user_id = value

    @property
    def user_name(self):
        return self._user_name

    @user_name.setter
    def user_name(self, value):
        self._user_name = value

    @property
    def user_picture(self):
        return self._user_picture

    @user_picture.setter
    def user_picture(self, value):
        self._user_picture = value

    def to_dict(self):
        return {k[1:]: v for k, v in vars(self).items()}

    @staticmethod
    def from_dict(advert_dict: dict):
        return Advert(id=advert_dict['id'],
                      title=advert_dict['title'],
                      image=advert_dict['image'],
                      description=advert_dict['description'],
                      start_date=advert_dict['start_date'],
                      end_date=advert_dict['end_date'],
                      location=advert_dict['location'],
                      price=advert_dict['price'],
                      availability=advert_dict['availability'],
                      user_id=advert_dict['user_id'],
                      user_name=advert_dict['user_name'],
                      user_picture=advert_dict['user_picture']
                      )

    def __repr__(self):
        return f"Advert{str(vars(self))}"
