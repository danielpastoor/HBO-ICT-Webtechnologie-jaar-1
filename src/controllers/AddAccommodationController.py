""" Index Controller
"""
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class AddAccommodationController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    @login_required
    def index(self):
        """ Endpoint for getting the profile page
        """

        return render_template("pages/dashboard/addaccommodation.html")


if __name__ == "__main__":
    pass
