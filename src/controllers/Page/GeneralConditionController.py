""" General Condiation Controller
"""
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class GeneralConditionController(ControllerBase):
    """general controller for showing the general condition page

    Returns:
        _type_: page
    """

    @login_required
    def index(self):
        """ Endpoint for getting the General condition page
        """

        return render_template("pages/general/general-conditions.html")


if __name__ == "__main__":
    pass
