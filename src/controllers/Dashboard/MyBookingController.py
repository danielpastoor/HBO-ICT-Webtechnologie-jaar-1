""" My Booking Controller
"""

from flask import render_template
from flask_login import login_required, current_user

from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BookingEntity import BookingEntity


class MyBookingController(ControllerBase):

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    def index(self):
        # Fetch the current user's username
        current_username = current_user.get_id()  # Assuming get_id() returns the username

        # Fetch the numeric user_id for the current user using the username
        user_id = self.app_context.get_user_id_by_username(current_username)

        if user_id:
            join_clause = "LEFT JOIN accommodation ON booking.accommodation_id = accommodation.id"
            bookings = self.app_context.Get(BookingEntity(),
                                              "booking.*, accommodation.name, "
                                              "accommodation.thumbnail_image",
                                              f"booking.user_id = {user_id}", join_clause)
        else:
            bookings = []
            # Handle case where user_id is not found

        # Return rendered HTML with bookings data
        return render_template("pages/dashboard/dashboard.html", bookings=bookings, )


if __name__ == "__main__":
    pass
