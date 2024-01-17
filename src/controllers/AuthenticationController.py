""" Index Controller
"""
# needed imports
from flask import render_template, request, redirect, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
import logging

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, is_password_complex
from src.data.ApplicationContext import ApplicationContext
from src.data.UserEntity import UserEntity


class LoginPage(ControllerBase):

    def __init__(self):
        self.auth_processor = AuthenticationProcessor()

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
        user = self.auth_processor.validate_credentials(username, password)

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


class AuthenticationProcessor:
    MAX_LOGIN_ATTEMPTS = 5  # Maximaal toegestane inlogpogingen

    def __init__(self):
        self.app_context = ApplicationContext()
        self.failed_login_attempts = {}  # Houdt mislukte inlogpogingen bij

    def validate_credentials(self, username, password):
        """
        Valideert de inloggegevens van de gebruiker. """

        user = self.app_context.get_user_by_username(username)

        # Controleer of de gebruiker bestaat
        if not user:
            logging.warning(f"Inlogpoging voor niet-bestaande gebruiker: {username}")
            return None

        # Controleer op te veel mislukte inlogpogingen
        if self.failed_login_attempts.get(username, 0) >= self.MAX_LOGIN_ATTEMPTS:
            logging.warning(f"Account vergrendeld wegens te veel mislukte inlogpogingen: {username}")
            return None

        # Valideer het wachtwoord
        if check_password_hash(user.password, password):
            logging.info(f"Gebruiker {username} succesvol ingelogd")
            self.failed_login_attempts[username] = 0  # Reset de teller bij succesvolle inlog
            return user
        else:
            # Verhoog het aantal mislukte inlogpogingen
            self.failed_login_attempts[username] = self.failed_login_attempts.get(username, 0) + 1
            logging.warning(f"Onjuiste wachtwoordpoging voor gebruiker: {username}")
            return None


class ResetPasswordController(ControllerBase):

    def get(self):
        """ Render the reset password page """
        return render_template('pages/reset-password.html')

    def post(self):
        """ Handle the reset password POST request """
        app_context = ApplicationContext()

        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validate and hash the password
        if password != confirm_password:
            flash("Passwords do not match", "error")
            return render_template('pages/reset-password.html')

        if not is_password_complex(password):
            flash("Password is not complex enough", "error")
            return render_template('pages/reset-password.html')

        user = app_context.get_user_by_username(username)

        if user is None:
            flash("User not found", "error")
            return render_template('pages/reset-password.html')

        # Update the user's password
        success = app_context.update_user_password(username, password)

        if success:
            flash("Password reset successful", "success")
            return redirect("/login")
        else:
            flash("Password reset failed", "error")
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

        if not is_password_complex(password):
            flash("Password is not complex enough", "error")
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
