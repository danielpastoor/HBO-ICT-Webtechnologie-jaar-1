import datetime
from flask import request, jsonify
from flask_login import current_user

from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.ChatMessageEntity import ChatMessageEntity

class ChatController(ControllerBase):
    route_base = "/dashboard/save-chat"

    def __init__(self):
        self.app_context = ApplicationContext()

    def post(self):
        username = current_user.get_id() if current_user.is_authenticated else None

        if username:
            user_id = self.app_context.get_user_id_by_username(username)
        else:
            user_id = None

        data = request.json
        user_id = user_id  # This should be an integer or None
        email = data.get('email')  # This should be a string or empty
        name = data.get('name')  # This should be a string or empty
        message = data.get('message')
        timestamp = datetime.datetime.now()

        # Maak ChatMessageEntity object
        chat_message = ChatMessageEntity(user_id, email, name, message, timestamp)

        # Sla het bericht op in de database
        success = self.app_context.save_chat_message(chat_message)

        if success:
            return jsonify({"message": "Chatbericht opgeslagen"}), 200
        else:
            return jsonify({"message": "Fout bij het opslaan van chatbericht"}), 500