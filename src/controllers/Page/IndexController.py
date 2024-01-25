""" Index Controller
"""
# needed imports
from flask import render_template

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity


class IndexController(ControllerBase):
    """general controller for showing the home page

    Returns:
        _type_: page
    """

    def __init__(self):
        self.app_context = ApplicationContext()

    def index(self):
        """ Endpoint for getting the general page
        """
        # Get popular accommodation
        accommodation = self.app_context.First(AccommodationEntity(),
                                                 "accommodation.*, COUNT(booking.id) AS booking_count",
                                                 None,
                                                 """
                                                 LEFT JOIN booking ON accommodation.id = booking.accommodation_id
                                                 GROUP BY accommodation.Id
                                                 ORDER BY booking_count DESC
                                                 LIMIT 1
                                                 """
                                                 )

        # get accommodations for the slider
        accommodations = self.app_context.Get(AccommodationEntity())

        # return rendered html
        return render_template("pages/general/index.html", accommodation=accommodation, accommodations=accommodations,
                               found_items=len(accommodations))


if __name__ == "__main__":
    pass
