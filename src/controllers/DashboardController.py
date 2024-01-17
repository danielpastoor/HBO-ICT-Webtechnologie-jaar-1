""" Index Controller
"""
import flask_login
# needed imports
from flask import render_template, redirect, flash
from flask_login import login_required, current_user

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class DashboardController(ControllerBase):

    @login_required
    def index(self):
        applicationContext = ApplicationContext()

        # Fetch the current user's details
        current_username = current_user.get_id()  # Assuming get_id() returns the username
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

        # Return rendered HTML with bookings data and isAdmin flag
        return render_template("pages/dashboard/dashboard.html", bookings=bookings, isAdmin=isAdmin)


if __name__ == "__main__":
    pass
