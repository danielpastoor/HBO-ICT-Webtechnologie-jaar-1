from src.models.BaseModel.BaseEntity import BaseEntity


class AccommodationEntity(BaseEntity):
    def __init__(self):
        pass

    # Booking date

    @property
    def name(self) -> str:
        return self.GetValue("name")

    @name.setter
    def name(self, value: str) -> None:
        self.SetValue("name", value)

    # accommodation price
    @property
    def max_persons(self) -> int:
        return self.GetValue("max_persons")

    @max_persons.setter
    def max_persons(self, value: int) -> None:
        self.SetValue("max_persons", value)

    # accommodation price
    @property
    def price(self) -> float:
        return self.GetValue("price")

    @price.setter
    def price(self, value: float) -> None:
        self.SetValue("price", value)

    # accommodation description
    @property
    def description(self) -> str:
        return self.GetValue("description")

    @description.setter
    def description(self, value: str) -> None:
        self.SetValue("description", value)