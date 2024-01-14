""" Index Controller
"""
import flask_login
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class DashboardController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    @login_required
    # get
    def index(self):
        """ Endpoint for getting the index page
        """

        # print(flask_login.current_user)
        #
        # applicationContext = ApplicationContext()
        #
        # bookings = applicationContext.Get(BookingEntity(), "*", f"id = {flask_login.current_user.id}")

        # return rendered html
        return render_template("pages/dashboard/dashboard.html", bookings=[])




if __name__ == "__main__":
    pass
