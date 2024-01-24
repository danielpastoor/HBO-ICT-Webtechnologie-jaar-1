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

    # accommodation description
    @property
    def location(self) -> str:
        return self.GetValue("location")

    @location.setter
    def location(self, value: str) -> None:
        self.SetValue("location", value)

    # accommodation description
    @property
    def thumbnail_image(self) -> str:
        return self.GetValue("thumbnail_image", "/static/img/default-accomodation.jpg")

    @thumbnail_image.setter
    def thumbnail_image(self, value: str) -> None:
        self.SetValue("thumbnail_image", value)

    @property
    def images(self) -> str:
        return self.GetValue("images", "/static/img/default-accomodation.jpg")

    @images.setter
    def images(self, value: str) -> None:
        self.SetValue("images", value)
    def get_images(self):
        return self.images.split(';')

    def get_images_count(self) -> int:
        return len(self.get_images())
