from flask import render_template, jsonify, request
from flask_login import login_required, current_user

from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BookingEntity import BookingEntity


class MyBookingController(ControllerBase):

    @login_required
    def index(self):
        applicationContext = ApplicationContext()

        # Fetch the current user's username
        current_username = current_user.get_id()  # Assuming get_id() returns the username

        # Fetch the numeric user_id for the current user using the username
        user_id = applicationContext.get_user_id_by_username(current_username)
        if user_id:
            join_clause = "LEFT JOIN accommodation ON booking.accommodation_id = accommodation.id"
            bookings = applicationContext.Get(BookingEntity(),
                                              "booking.*, accommodation.name, "
                                              "accommodation.thumbnail_image",
                                              f"booking.user_id = {user_id}", join_clause)
        else:
            bookings = []
            # Handle case where user_id is not found

        # Return rendered HTML with bookings data
        return render_template("pages/dashboard/booked-trips.html", bookings=bookings, )

    def post(self):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'message': 'User not authenticated'})

        data = request.get_json()
        start_date = data.get('startDate')
        end_date = data.get('endDate')

        # Add your logic to handle the booking

        return jsonify({'success': True, 'message': 'Booking processed'})


if __name__ == "__main__":
    pass
