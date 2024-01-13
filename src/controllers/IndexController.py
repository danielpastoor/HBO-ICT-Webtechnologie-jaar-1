""" Index Controller
"""
# needed imports
from flask import render_template, request
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class IndexController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        # user_cookie = request.cookies.get('user_cookie') #TODO: revisite later
        # if user_cookie:
        # Perform actions based on the user_cookie

        # return rendered html
        return render_template("pages/index.html")


if __name__ == "__main__":
    pass
