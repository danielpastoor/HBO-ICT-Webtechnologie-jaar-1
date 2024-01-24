from flask_login import UserMixin
from src.models.BaseModel.TransientObject import TransientObject


class UserClaimsPrincipal(UserMixin, TransientObject):
    __tablename__ = 'users'

    def __init__(self, username, email, password, city, postcode, address, housenumber, is_admin=False):
        if not username:
            raise ValueError("Username cannot be empty")
        if not email:
            raise ValueError("Email cannot be empty")

        self.username = username
        self.email = email
        self.password = password  # Ensure password is hashed before setting
        self.city = city
        self.postcode = postcode
        self.address = address
        self.housenumber = housenumber
        self.is_admin = is_admin  # Admin flag

    def GetCurrent(self):
        return {
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'city': self.city,
            'postcode': self.postcode,
            'address': self.address,
            'housenumber': self.housenumber,
            'is_admin': self.is_admin
        }

    def get_id(self):
        return self.username
