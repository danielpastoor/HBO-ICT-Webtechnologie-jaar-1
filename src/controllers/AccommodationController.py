""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity


class AccommodationController(ControllerBase):
    """PricingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        applicationContext = ApplicationContext()

        # SELECT * FROM table_name
        data = applicationContext.Get(AccommodationEntity())

        # return rendered html
        return render_template("pages/accommodation.html", accommodations=data)

if __name__ == "__main__":
    pass
