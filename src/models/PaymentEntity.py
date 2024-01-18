from src.models.BaseModel.BaseEntity import BaseEntity
from src.models.Enums.PaymentStatus import PaymentStatus


class PaymentEntity(BaseEntity):
    # Name of the person
    @property
    def status(self) -> PaymentStatus:
        return self.GetValue("status")

    @status.setter
    def status(self, value: PaymentStatus) -> None:
        self.SetValue("status", value)

    # Name of the person
    @property
    def price(self) -> int:
        return self.GetValue("price")

    @price.setter
    def price(self, value: int) -> None:
        self.SetValue("price", value)
