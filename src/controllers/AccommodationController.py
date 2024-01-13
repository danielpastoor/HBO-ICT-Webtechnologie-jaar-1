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
        return render_template("pages/accommodation/accommodationOverview.html", accommodations=data)

    def accommodation(self, accommodation_id):
        """ Endpoint for getting the index page
        """
        applicationContext = ApplicationContext()

        data = applicationContext.Get(AccommodationEntity(), condition=f"id = {accommodation_id}")

        if len(data) != 1:
            return "There went something wrong", 500

        # return rendered html
        return render_template("pages/accommodation/accommodationDetail.html", accommodation=data[0])


if __name__ == "__main__":
    pass
