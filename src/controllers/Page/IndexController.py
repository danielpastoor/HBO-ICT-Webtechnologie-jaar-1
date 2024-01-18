""" Index Controller
"""
# needed imports
from flask import render_template, request
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class IndexController(ControllerBase):
    """general controller for showing the home page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the general page
        """
        # user_cookie = request.cookies.get('user_cookie') #TODO: revisite later
        # if user_cookie:
        # Perform actions based on the user_cookie

        applicationContext = ApplicationContext()

        # Get popular accommodation
        accommodation = applicationContext.First(AccommodationEntity(),
                                                 "accommodation.*, COUNT(booking.id) AS booking_count",
                                                 None,
                                                 """
                                                 LEFT JOIN booking ON accommodation.id = booking.accommodation_id
                                                 GROUP BY accommodation.Id
                                                 ORDER BY booking_count DESC
                                                 LIMIT 1
                                                 """
                                                 )

        accommodations = applicationContext.Get(AccommodationEntity())

        # return rendered html
        return render_template("pages/general/index.html", accommodation=accommodation, accommodations=accommodations,
                               found_items=len(accommodations))


if __name__ == "__main__":
    pass
