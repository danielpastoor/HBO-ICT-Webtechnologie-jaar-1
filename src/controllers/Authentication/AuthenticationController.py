""" Authentication Controller
"""

import logging
import re

# needed imports
from flask import render_template, request, redirect, flash, make_response
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods
from src.data.ApplicationContext import ApplicationContext
from src.data.UserClaimsPrincipal import UserClaimsPrincipal
from src.models.UsersEntity import UsersEntity


class AuthenticationController(ControllerBase):

    def __init__(self):
        self.auth_processor = AuthenticationProcessor()
        self.app_context = ApplicationContext()

    def index(self):
        """ Endpoint for getting the login page """
        if current_user.is_authenticated:
            # If user is already logged in, redirect to a different page
            return redirect('/')

        return render_template("pages/authentication/authentication.html")

    @RouteMethods(["POST"])
    def login(self):
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
            flash("Inloggen gelukt!", "success")
            return response
        else:
            # Login failed
            flash("Ongeldige gebruikersnaam of wachtwoord!", "error")
            return redirect('/authentication')

    @RouteMethods(["GET", "POST"])
    def resetpassword(self):
        if request.method == "GET":
            """ Render the reset password page """
            return render_template('pages/authentication/reset-password.html')

        elif request.method == "POST":
            """ Handle the reset password POST request """
            username = request.form.get('username')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')

            # Validate and hash the password
            if password != confirm_password:
                flash("Wachtwoorden komen niet overeen", "error")
                return redirect('/authentication/resetpassword')

            if not self.__is_password_complex(password):
                flash("Wachtwoord is niet complex genoeg", "error")
                return redirect('/authentication/resetpassword')

            user = self.app_context.get_user_by_username(username)

            if user is None:
                flash("Gebruiker niet gevonden", "error")
                return redirect('/authentication/resetpassword')

            # Update the user's password
            success = self.app_context.update_user_password(username, password)

            if success:
                flash("Wachtwoord resetten succesvol", "success")
                return redirect('/authentication')
            else:
                flash("Wachtwoord resetten mislukt", "error")
                return redirect('/authentication/resetpassword')

    @login_required
    def logout(self):
        """Handle the logout process."""
        logout_user()
        flash("Je bent uitgelogd.", "info")
        return redirect('/authentication')  # Redirect to the general page or your chosen login page

    @RouteMethods(["GET", "POST"])
    def register(self):
        if request.method == "GET":
            # # Default to handling GET request
            return render_template('pages/authentication/authentication.html', is_register=True)

        elif request.method == "POST":
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
                flash("Wachtwoorden komen niet overeen", "error")
                return redirect('/authentication/register')

            if not self.__is_password_complex(password):
                flash("Wachtwoord is niet complex genoeg", "error")
                return redirect('/authentication/register')

            if self.app_context.First(UsersEntity(),
                                      condition=f"username = '{username}' or email = '{email}'") is not None:
                flash("Gebruiker bestaat al", "error")
                return redirect('/authentication/register')

            hashed_password = generate_password_hash(password)

            # Create a new user entity with the hashed password
            new_user = UserClaimsPrincipal(username, email, hashed_password, city, postcode, address, housenumber)

            # Attempt to add the new user to the database
            try:
                self.app_context.Add(new_user)
                flash("Registratie geslaagd!", "success")
                return redirect('/authentication')

            except Exception as e:
                flash("Registratie mislukt: " + str(e), "error")
                return redirect('/authentication/register')

    def __is_password_complex(self, password):
        """Check if the password is complex enough."""
        min_length = 8
        if len(password) < min_length:
            return False
        if not re.search(r"[0-9]", password):
            return False
        if not re.search(r"[A-Z]", password):
            return False
        if not re.search(r"[a-z]", password):
            return False
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            return False
        return True


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


if __name__ == "__main__":
    pass
