from src.models.BaseModel.TransientObject import TransientObject


class UserEntity(TransientObject):
    __tablename__ = 'users'

    def __init__(self, username, email, password, city, postcode, address, housenumber):
        if not username:
            raise ValueError("Username cannot be empty")
        if not email:
            raise ValueError("Email cannot be empty")
        if not password:
            raise ValueError("Password cannot be empty")
        # Add similar checks for other fields if necessary

        self.username = username
        self.email = email
        self.password = password  # Make sure to hash the password before setting it
        self.city = city
        self.postcode = postcode
        self.address = address
        self.housenumber = housenumber

    def GetCurrent(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'city': self.city,
            'postcode': self.postcode,
            'address': self.address,
            'housenumber': self.housenumber
        }
