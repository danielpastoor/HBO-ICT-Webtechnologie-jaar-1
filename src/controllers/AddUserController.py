""" Index Controller
"""
# needed imports
from flask import render_template, request, flash, redirect
from flask_login import login_required
from werkzeug.security import generate_password_hash

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext


class AddUserController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    @login_required
    def get(self):
        app_context = ApplicationContext()
        users = app_context.get_all_users()

        return render_template("pages/dashboard/adduser.html", users=users)

    def post(self):
        if request.method == 'POST':
            # Extract data from form
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            city = request.form.get('city')
            postcode = request.form.get('postcode')
            address = request.form.get('address')
            housenumber = request.form.get('housenumber')
            is_admin = request.form.get('is_admin')

            # Validate data (e.g., check if passwords match)
            if password != confirm_password:
                flash("Passwords do not match.", "error")
                return redirect('/submit-new-user')

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

            # Use ApplicationContext to register the user
            app_context = ApplicationContext()

            # Attempt to add the new user to the database
            try:
                app_context.register_user(user_data)
                flash("Registration successful!", "success")
                return redirect('/submit-new-user')

            except Exception as e:
                flash("Registration failed: " + str(e), "error")
                return render_template('pages/dashboard/dashboard.html')

        return render_template("pages/dashboard/adduser.html")  # Render the registration form for GET request


if __name__ == "__main__":
    pass
