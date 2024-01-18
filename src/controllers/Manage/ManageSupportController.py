""" Index Controller
"""
# needed imports
from flask import render_template, session
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class ManageSupportController(ControllerBase):

    @login_required
    def index(self):
        app_context = ApplicationContext()
        chat_messages = app_context.get_all_chat_messages()  # Method to fetch all chat messages

        return render_template("pages/manage/manage-support.html", chat_messages=chat_messages)


if __name__ == "__main__":
    pass
