""" Profile Controller
"""
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class ProfileController(ControllerBase):
    """general controller for showing the setting page

    Returns:
        _type_: page
    """

    @login_required
    def index(self):
        """ Endpoint for getting the profile page
        """

        return render_template("pages/dashboard/dashboard-profile.html")


if __name__ == "__main__":
    pass
