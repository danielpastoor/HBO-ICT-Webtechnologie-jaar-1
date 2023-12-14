""" Index Controller
"""
# needed imports
from flask import render_template, request
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import BookingEntity
from src.models.BaseModel.TransientObject import TransientObject


class IndexController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        # SELECT * FROM table_name
        data = applicationContext.Get(BookingEntity())


        # return rendered html
        return render_template("pages/index.html", data=data)

if __name__ == "__main__":
    pass
