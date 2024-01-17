from datetime import datetime

from src.models.BaseModel.TransientObject import TransientObject


class ChatMessageEntity(TransientObject):
    __tablename__ = 'chat_messages'

    def __init__(self, user_id=None, email=None, name=None, message=None, timestamp=None):
        self.user_id = user_id
        self.email = email
        self.name = name
        self.message = message
        self.timestamp = timestamp if timestamp else datetime.now()

    def GetCurrent(self):
        """Return the current state as a dictionary."""
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'message': self.message,
            'timestamp': self.timestamp
        }

    def __repr__(self):
        return f"<ChatMessageEntity(user_id={self.user_id}, email='{self.email}', name='{self.name}', message='{self.message}', timestamp={self.timestamp})>"
