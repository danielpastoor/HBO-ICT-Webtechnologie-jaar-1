""" Index Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext


class ManageUserController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    def __init__(self):
        """
        Initialize the controller with the Flask app and set up routes.
        """
        self.app_context = ApplicationContext()

    @login_required
    def get(self):
        app_context = ApplicationContext()
        users = app_context.get_all_users()

        return render_template("pages/admin-dashboard/admin-dashboard-add-user.html", users=users)

    @login_required
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
            return redirect('/dashboard/submit-new-user')

        # Hash the password
        hashed_password = generate_password_hash(password)
        print("Is Admin:", is_admin)
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

        # Use ApplicationContext to register the user
        app_context = ApplicationContext()

        # Attempt to add the new user to the database
        try:
            app_context.register_user(user_data)
            flash("Registration successful!", "success")
            return redirect('/dashboard/submit-new-user')

        except Exception as e:
            flash("Registration failed: " + str(e), "error")
            return render_template('pages/admin-dashboard/admin-dashboard-add-user.html')

    @login_required
    def delete_user(self, user_id):
        if not current_user.is_admin:
            flash("You do not have permission to perform this action.", "error")
            return redirect('/dashboard/submit-new-user')  # Redirect to a safe page

        if self.__delete_user(user_id):
            flash("User successfully removed.", "success")
        else:
            flash("Failed to remove user.", "error")

        return redirect('/dashboard/submit-new-user')  # Redirect to the users list page

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

    @login_required
    def register(self, user_id=None):
        app_context = ApplicationContext()
        users = app_context.get_all_usersnamess()

        user_to_edit = None
        if user_id:
            # Fetch user details for editing
            user_to_edit = app_context.get_user_id_by_username(user_id)
            if not user_to_edit:
                flash("User not found.", "error")
                return redirect('/dashboard/submit-new-user/')  # Adjust as per your route naming

        return render_template("pages/admin-dashboard/admin-dashboard-register-user.html", users=users,
                               user=user_to_edit)


if __name__ == "__main__":
    pass
