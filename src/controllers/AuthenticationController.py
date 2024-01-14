""" Index Controller
"""
# needed imports
from flask import render_template, request, redirect, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods
from src.data.ApplicationContext import ApplicationContext
from src.data.UserEntity import UserEntity
from src.models.UsersEntity import UsersEntity


class LoginPage(ControllerBase):

    def index(self):
        """ Endpoint for getting the login page """
        if current_user.is_authenticated:
            # If user is already logged in, redirect to a different page
            return redirect('/')

        return render_template("pages/login.html")

    def post(self):
        """ Endpoint for handling login POST request """
        username = request.form.get('username')
        password = request.form.get('password')

        remember = 'remember_me' in request.form

        # Logic to validate user credentials
        user = self.validate_credentials(username, password)

        if user:
            # Login successful: set up the user session, etc.
            login_user(user, remember=remember)
            # Create a response and set a cookie
            response = make_response(redirect('/'))
            # Set a cookie with the user's username
            response.set_cookie('user_cookie', user.username, max_age=60 * 60 * 24 * 30)  # Expires in 30 days
            flash("Login successful!", "success")
            return response
        else:
            # Login failed
            flash("Invalid username or password", "error")
            return render_template("pages/login.html")

    def validate_credentials(self, username, password):
        app_context = ApplicationContext()
        user = app_context.get_user_by_username(username)

        if not user or not user.password:
            return None

        if user and check_password_hash(user.password, password):
            return user
        return None

    @RouteMethods(["GET", "POST"])
    def ResetPassword(self):

        if request.method == "POST":
            app_context = ApplicationContext()

            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Validate and hash the password
            if password != confirm_password:
                flash("Passwords do not match", "error")
                return render_template('pages/reset-password.html')

            user = app_context.get_user_by_username(username)

            if user is None:
                return render_template('pages/error.html')

            update_data = {"password": generate_password_hash(password)}

            app_context.Update(UsersEntity(), update_data, user.id)

            return redirect("/login")
        else:
            return render_template('pages/reset-password.html')


class LogoutPage(ControllerBase):

    @login_required
    def get(self):
        """Handle the logout process."""
        logout_user()
        flash("You have been logged out.", "info")
        # Create a response
        response = make_response(redirect('/login'))
        return response  # Redirect to the index page or your chosen login page


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
