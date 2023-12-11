""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class LoginPage(ControllerBase):
    """LoginPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        # return rendered html
        return render_template("pages/login.html")


class RegisterPage(ControllerBase):
    """RegisterPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        # return rendered html
        return render_template("pages/register.html")


if __name__ == "__main__":
    pass
