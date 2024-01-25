""" Manage User Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods, check_is_admin
from src.data.ApplicationContext import ApplicationContext
from src.models.UsersEntity import UsersEntity


class ManageUserController(ControllerBase):

    def __init__(self):
        """
        Initialize the controller with the Flask app and set up routes.
        """
        self.app_context = ApplicationContext()

    @login_required
    @check_is_admin
    def get(self):
        # get all users
        users = self.app_context.get_all_users()

        return render_template("pages/manage/manage-user.html", users=users)

    @login_required
    @check_is_admin
    def post(self):
        # Extract data from form
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        address = request.form.get('address')
        housenumber = request.form.get('housenumber')
        is_admin = 1 if request.form.get('is_admin') == 'on' else 0  # Correctly format is_admin

        # Validate data (e.g., check if passwords match)
        if password != confirm_password:
            flash("Passwords do not match.", "error")
            return redirect('/manage/users')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a user dictionary
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password,
            "city": city,
            "postcode": postcode,
            "address": address,
            "housenumber": housenumber,
            "is_admin": is_admin
        }

        # Attempt to add the new user to the database
        try:
            self.app_context.register_user(user_data)
            flash("Registratie geslaagd!", "success")
            return redirect('/manage/users')

        except Exception as e:
            flash("Registratie mislukt: " + str(e), "error")
            return redirect('/manage/users')

    @login_required
    @check_is_admin
    def delete_user(self, user_id):
        if not current_user.is_admin:
            flash("Je hebt hier niet genoeg rechten voor.", "error")
            return redirect('/manage/users')  # Redirect to a safe page

        if self.__delete_user(user_id):
            flash("Gebruiker succesvol verwijderd.", "success")
        else:
            flash("Gebruiker niet verwijderd.", "error")

        return redirect('/manage/users')  # Redirect to the users list page

    def __delete_user(self, user_id):
        """
        Delete a user from the database.
        """
        try:
            self.app_context.delete_user(user_id)
            return True
        except Exception as e:
            print(f"Error removing user: {e}")
            return False

    @RouteMethods(["GET", "POST"])
    @login_required
    @check_is_admin
    def edit(self, user_name):
        if request.method == "GET":
            # Fetch user details for editing
            user_to_edit = self.app_context.get_user_by_username(user_name)
            if not user_to_edit:
                flash("Gebruiker is niet gevonden.", "error")
                return redirect('/manage/users')  # Adjust as per your route naming

            return render_template("pages/manage/manage-edit-user.html",
                                   user=user_to_edit)

        elif request.method == "POST":
            # Extract data from form
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            city = request.form.get('city')
            postcode = request.form.get('postcode')
            address = request.form.get('address')
            housenumber = request.form.get('housenumber')
            is_admin = 1 if request.form.get('is_admin') == 'on' else 0  # Correctly format is_admin

            user_data = {
                "username": username,
                "email": email,
                "city": city,
                "postcode": postcode,
                "address": address,
                "housenumber": housenumber,
                "is_admin": is_admin
            }

            # Validate data (e.g., check if passwords match)
            if password and password != confirm_password:
                flash("Wachtwoorden komen niet overeen.", "error")
                return redirect('/manage/users')
            elif password:
                # Hash the password
                hashed_password = generate_password_hash(password)
                user_data["password"] = hashed_password

            user_id = self.app_context.get_user_id_by_username(username)

            # Attempt to add the new user to the database
            try:
                self.app_context.Update(UsersEntity(), user_data, user_id)
                flash("Registratie geslaagd!", "success")
                return redirect('/manage/users')

            except Exception as e:
                flash("Registratie mislukt: " + str(e), "error")
                return redirect('/manage/users')


if __name__ == "__main__":
    pass
