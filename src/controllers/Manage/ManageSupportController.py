""" Manage Support Controller
"""
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext


class ManageSupportController(ControllerBase):

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    def index(self):
        contact_messages = self.app_context.get_all_contact_messages()  # Method to fetch all chat messages

        return render_template("pages/manage/manage-support.html", contact_messages=contact_messages)


if __name__ == "__main__":
    pass
