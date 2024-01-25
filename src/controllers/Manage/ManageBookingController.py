""" Booking Controller
"""
# needed imports
from flask import render_template, redirect, flash, request
from flask_login import login_required, current_user

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods, check_is_admin
from src.data.ApplicationContext import ApplicationContext
from src.models.BookingEntity import BookingEntity


class ManageBookingController(ControllerBase):

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    @check_is_admin
    def get(self):
        users = self.app_context.get_all_usersnamess()  # Fetch all users
        accommodations = self.app_context.get_all_accommodations()  # Fetch all accommodations

        # Fetch the current user's details
        current_username = current_user.get_id()
        current_user_details = self.app_context.get_user_by_username(current_username)

        # Set isAdmin based on the user's admin status
        isAdmin = current_user_details.is_admin if current_user_details else False

        if isAdmin:
            # Fetch all bookings for admin
            join_clause = "LEFT JOIN accommodation ON booking.accommodation_id = accommodation.id"
            bookings = self.app_context.Get(BookingEntity(),
                                              "booking.*, accommodation.name, "
                                              "accommodation.thumbnail_image",
                                              join=join_clause)
        else:
            # Redirect non-admin users or show an error message
            flash("Je hebt hier niet genoeg rechten voor..", "error")
            return redirect('/accommodation')  # Redirect to a different page

        # Render the dashboard template
        return render_template("pages/manage/manage-booking.html", bookings=bookings, isAdmin=isAdmin,
                               accommodations=accommodations, users=users)

    @login_required
    @check_is_admin
    def post(self):

        # Handle booking form submission
        booking_data = {
            'user_id': request.form.get('user_id'),
            'start_date': request.form.get('start_date'),
            'end_date': request.form.get('end_date'),
            'accommodation_id': request.form.get('accommodation_id'),
            'special_requests': request.form.get('specialRequests')
        }

        if self.app_context.submit_booking(booking_data):
            flash("Boeking succesvol ingediend.", "success")
        else:
            flash("Boeking niet verzonden.", "error")

        # Redirect back to the dashboard or appropriate page after handling POST
        return redirect('/manage/bookings')  # or the URL of your choice

    @login_required
    @check_is_admin
    def delete_booking(self, id):
        if not current_user.is_admin:
            flash("Je hebt hier niet genoeg rechten voor.", "error")
            return redirect('/manage/bookings')  # Redirect to a safe page

        if self.__delete_booking(id):
            flash("Booking is verwijderd.", "success")
        else:
            flash("Gefaald om booking te verwijderen.", "error")

        return redirect('/manage/bookings')  # Redirect to the users list page

    def __delete_booking(self, id):
        """
        Delete an booking from the database.
        """

        try:
            self.app_context.Delete(BookingEntity(), id)
            return True
        except Exception as e:
            print(f"Error removing booking: {e}")
            return False

    @RouteMethods(["GET", "POST"])
    @login_required
    @check_is_admin
    def edit(self, id):
        if request.method == "GET":
            # Fetch user details for editing
            booking_to_edit = self.app_context.First(BookingEntity(), condition=f"id = {id}")
            accommodations = self.app_context.get_all_accommodations()  # Fetch all accommodations

            if not booking_to_edit:
                flash("Boeking niet gevonden.", "error")
                return redirect('/manage/bookings')  # Adjust as per your route naming

            return render_template("pages/manage/manage-edit-booking.html",
                                   booking=booking_to_edit, accommodations=accommodations)

        elif request.method == "POST":
            booking_data = {
                'start_date': request.form.get('start_date'),
                'end_date': request.form.get('end_date'),
                'accommodation_id': request.form.get('accommodation_id'),
                'special_requests': request.form.get('specialRequests')
            }

            self.app_context.Update(BookingEntity(), booking_data, id)

            flash("Booking is geupdate.", "success")

            # Redirect back to the dashboard or appropriate page after handling POST
            return redirect('/manage/bookings')


if __name__ == "__main__":
    pass
