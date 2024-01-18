""" Index Controller
"""
import flask_login
# needed imports
from flask import render_template, redirect, flash, request
from flask_login import login_required, current_user

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class DashboardController(ControllerBase):

    @login_required
    def get(self):
        applicationContext = ApplicationContext()

        users = applicationContext.get_all_usersnamess()  # Fetch all users
        accommodations = applicationContext.get_all_accommodations()  # Fetch all accommodations

        # Fetch the current user's details
        current_username = current_user.get_id()
        current_user_details = applicationContext.get_user_by_username(current_username)

        # Set isAdmin based on the user's admin status
        isAdmin = current_user_details.is_admin if current_user_details else False

        if isAdmin:
            # Fetch all bookings for admin
            bookings = applicationContext.Get(BookingEntity(), "*")
        else:
            # Redirect non-admin users or show an error message
            flash("You do not have permission to access this page.", "error")
            return redirect('/accommodation')  # Redirect to a different page

        # Render the dashboard template
        return render_template("pages/admin-dashboard/admin-dashboard-booked.html", bookings=bookings, isAdmin=isAdmin,
                               accommodations=accommodations, users=users)

    @login_required
    def post(self):
        applicationContext = ApplicationContext()

        # Handle booking form submission
        booking_data = {
            'user_id': request.form.get('user_id'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'accommodation_id': request.form.get('accommodation_id'),
            'num_guests': request.form.get('numGuests'),
            'special_requests': request.form.get('specialRequests')
        }

        if applicationContext.submit_booking(booking_data):
            flash("Booking submitted successfully.", "success")
        else:
            flash("Failed to submit booking.", "error")

        # Redirect back to the dashboard or appropriate page after handling POST
        return redirect('/all-bookings')  # or the URL of your choice


if __name__ == "__main__":
    pass
