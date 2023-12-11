from datetime import datetime

from src.models.BaseModel.TransientObject import TransientObject


class BaseEntity(TransientObject):
    def __init__(self):
        pass

    # Primary Key
    @property
    def Id(self) -> int:
        return self.GetValue("Id")

    @Id.setter
    def Id(self, value: int) -> None:
        self.SetValue("Id", value)

    # Created At
    @property
    def Created_at(self) -> datetime:
        return self.GetValue("Created_at")

    @Created_at.setter
    def Created_at(self, value:datetime) -> None:
        self.SetValue("Id", value)

    # Modified At

    @property
    def Modified_at(self) -> datetime:
        return self.GetValue("Created_at")

    @Modified_at.setter
    def Modified_at(self, value: datetime) -> None:
        self.SetValue("Id", value)

