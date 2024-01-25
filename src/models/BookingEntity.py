from datetime import datetime

from src.models.BaseModel.BaseEntity import BaseEntity


class BookingEntity(BaseEntity):
    def __init__(self):
        pass

    # Booking date
    @property
    def payment_id(self) -> int:
        return self.GetValue("payment_id")

    @payment_id.setter
    def payment_id(self, value: int) -> None:
        self.SetValue("payment_id", value)

    # Booking date
    @property
    def booking_date(self) -> datetime:
        return self.GetValue("booking_date")

    @booking_date.setter
    def booking_date(self, value: datetime) -> None:
        self.SetValue("booking_date", value)

    # Start booking date
    @property
    def start_date(self) -> datetime:
        return self.GetValue("start_date")

    @start_date.setter
    def start_date(self, value: datetime) -> None:
        self.SetValue("start_date", value)

    # End booking date
    @property
    def end_date(self) -> datetime:
        return self.GetValue("end_date")

    @end_date.setter
    def end_date(self, value: datetime) -> None:
        self.SetValue("end_date", value)

    # User who booked
    @property
    def user_id(self) -> int:
        return self.GetValue("user_id")

    @user_id.setter
    def user_id(self, value: int) -> None:
        self.SetValue("user_id", value)

    # accommodation
    @property
    def accommodation_id(self) -> int:
        return self.GetValue("accommodation_id")

    @accommodation_id.setter
    def accommodation_id(self, value: int) -> None:
        self.SetValue("accommodation_id", value)

    # accommodation
    @property
    def special_requests(self) -> str:
        return self.GetValue("special_requests")

    @special_requests.setter
    def special_requests(self, value: str) -> None:
        self.SetValue("special_requests", value)


