""" Index Controller
"""
# needed imports
from flask import render_template
from flask.ctx import AppContext
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class RegisterUserController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """
    @login_required
    def get(self, user_id):
        app_context = ApplicationContext()
        users = app_context.get_all_users()

        return render_template("pages/dashboard/registeruser.html", users=users)


if __name__ == "__main__":
    pass
