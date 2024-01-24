from datetime import datetime

from src.models.BaseModel.TransientObject import TransientObject


class ContactMessageEntity(TransientObject):
    __tablename__ = 'contact_messages'

    def __init__(self, user_id=None, email=None, name=None, message=None, sent_on=None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.message = message
        self.sent_on = sent_on if sent_on else datetime.now()

    def GetCurrent(self):
        """Return the current state as a dictionary."""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'message': self.message,
            'sent_on': self.sent_on
        }

    def __repr__(self):
        return f"<ContactMessageEntity(user_id={self.user_id}, email='{self.email}', name='{self.name}', message='{self.message}', sent_on={self.sent_on})>"
