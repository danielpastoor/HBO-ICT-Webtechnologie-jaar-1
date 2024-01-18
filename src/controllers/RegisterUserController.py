""" Index Controller
"""
# needed imports
from flask import render_template, redirect, flash
from flask.ctx import AppContext
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BaseModel.TransientObject import TransientObject
from src.models.BookingEntity import BookingEntity


class RegisterUserController(ControllerBase):

    @login_required
    def get(self, user_id=None):
        app_context = ApplicationContext()
        users = app_context.get_all_usersnamess()

        user_to_edit = None
        if user_id:
            # Fetch user details for editing
            user_to_edit = app_context.get_user_id_by_username(user_id)
            if not user_to_edit:
                flash("User not found.", "error")
                return redirect('/submit-new-user/')  # Adjust as per your route naming

        return render_template("pages/admin-dashboard/admin-dashboard-register-user.html", users=users, user=user_to_edit)


if __name__ == "__main__":
    pass
