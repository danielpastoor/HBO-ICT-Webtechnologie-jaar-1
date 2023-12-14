from datetime import datetime

from src.models.BaseModel.TransientObject import TransientObject


class BaseEntity(TransientObject):
    def __init__(self):
        pass

    # Primary Key
    @property
    def id(self) -> int:
        return self.GetValue("id")

    @id.setter
    def id(self, value: int) -> None:
        self.SetValue("id", value)

    # Created At
    @property
    def created_at(self) -> datetime:
        return self.GetValue("created_at")

    @created_at.setter
    def Created_at(self, value:datetime) -> None:
        self.SetValue("created_at", value)

    # Modified At

    @property
    def modified_at(self) -> datetime:
        return self.GetValue("modified_at")

    @modified_at.setter
    def modified_at(self, value: datetime) -> None:
        self.SetValue("modified_at", value)

    def SetCreationDate(self):
        self.created_at = datetime.now()
        self.SetModificationDate()

    def SetModificationDate(self):
        self.modified_at = datetime.now()

