""" Index Controller
"""
# needed imports
from flask import render_template, request, redirect, flash
from werkzeug.security import check_password_hash, generate_password_hash
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.data.UserEntity import UserEntity


class LoginPage(ControllerBase):

    def index(self):
        """ Endpoint for getting the login page """
        return render_template("pages/login.html")

    def post(self):
        """ Endpoint for handling login POST request """
        username = request.form.get('username')
        password = request.form.get('password')

        # Logic to validate user credentials
        user = self.validate_credentials(username, password)
        if user:
            # Login successful: set up the user session, etc.
            flash("Login successful!", "success")
            return redirect('/accommodation')  # Redirect to home or another dashboard page
        else:
            # Login failed
            flash("Invalid username or password", "error")
            return render_template("pages/login.html")

    def validate_credentials(self, username, password):
        app_context = ApplicationContext()
        user = app_context.get_user_by_username(username)

        if user and 'password' in user:
            hashed_password = user['password']
            return check_password_hash(hashed_password, password)
        return False


class RegisterPage(ControllerBase):

    def index(self):
        # # Default to handling GET request
        return render_template('pages/register.html')

    def post(self):
        app_context = ApplicationContext()
        # Extract form data
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        city = request.form.get('city')
        postcode = request.form.get('postcode')
        address = request.form.get('address')
        housenumber = request.form.get('housenumber')

        # Validate and hash the password
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('pages/register.html')

        hashed_password = generate_password_hash(password)
        print(hashed_password)

        # Create a new user entity with the hashed password
        new_user = UserEntity(username, email, hashed_password, city, postcode, address, housenumber)
        print(new_user)

        # Attempt to add the new user to the database
        try:
            app_context.Add(new_user)
            flash("Registration successful!", "success")
            return redirect('/login')

        except Exception as e:
            flash("Registration failed: " + str(e), "error")
            return render_template('pages/register.html')


if __name__ == "__main__":
    pass
