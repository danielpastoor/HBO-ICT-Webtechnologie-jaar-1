""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity


class BookingPage(ControllerBase):
    """BookingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def book(self, accommodation_id):
        """ Endpoint for getting the index page
        """
        applicationContext = ApplicationContext()

        data = applicationContext.Get(AccommodationEntity(), condition= f"id = {accommodation_id}")

        if len(data) != 1:
            return "There went something wrong", 500

        # return rendered html
        return render_template("pages/booking.html", booking=data[0])


if __name__ == "__main__":
    pass
