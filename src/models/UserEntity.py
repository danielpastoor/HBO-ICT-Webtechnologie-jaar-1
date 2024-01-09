from datetime import datetime
from src.models.BaseModel.BaseEntity import BaseEntity

class UserEntity(BaseEntity):
    def __init__(self):
        pass

    # Name of the person
    @property
    def username(self) -> str:
        return self.GetValue("username")

    @username.setter
    def username(self, value: str) -> None:
        self.SetValue("username", value)

    # Email
    @property
    def email(self) -> str:
        return self.GetValue("email")

    @email.setter
    def email(self, value: str) -> None:
        self.SetValue("email", value)

    # password
    @property
    def password(self) -> str:
        return self.GetValue("password")

    @password.setter
    def password(self, value: str) -> None:
        self.SetValue("password", value)

    # City
    @property
    def city(self) -> str:
        return self.GetValue("city")

    @city.setter
    def city(self, value: str) -> None:
        self.SetValue("city", value)


    # adress
    @property
    def adress(self) -> str:
        return self.GetValue("adress")

    @adress.setter
    def adress(self, value: str) -> None:
        self.SetValue("adress", value)

    # house number
    @property
    def housenumber(self) -> str:
        return self.GetValue("housenumber")

    @housenumber.setter
    def housenumber(self, value: str) -> None:
        self.SetValue("housenumber", value)

    # Credit card
    @property
    def credit_card(self) -> str:
        return self.GetValue("credit_card")

    @credit_card.setter
    def credit_card(self, value: str) -> None:
        self.SetValue("credit_card", value)