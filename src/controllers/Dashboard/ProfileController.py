""" Profile Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.UsersEntity import UsersEntity


class ProfileController(ControllerBase):
    """general controller for showing the setting page

    Returns:
        _type_: page
    """

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    def index(self):
        """ Endpoint for getting the profile page
        """

        return render_template("pages/dashboard/dashboard-profile.html")

    @login_required
    def post(self):
        # Extract data from form
        email = request.form.get('email')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        address = request.form.get('address')
        housenumber = request.form.get('housenumber')

        user_data = {
            "email": email,
            "city": city,
            "postcode": postcode,
            "address": address,
            "housenumber": housenumber
        }

        user_id = self.app_context.get_user_id_by_username(current_user.get_id())

        # Attempt to add the new user to the database
        try:
            self.app_context.Update(UsersEntity(), user_data, user_id)
            flash("Updaten profiel instellingen  geslaagd!", "success")
            return redirect('/dashboard/settings')

        except Exception as e:
            flash("Updaten profiel instellingen mislukt: " + str(e), "error")
            return redirect('/dashboard/settings')


if __name__ == "__main__":
    pass
