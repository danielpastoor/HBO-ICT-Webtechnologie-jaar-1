""" Contact Controller
"""
import datetime
import re

# needed imports
from flask import render_template, request, flash, redirect

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.data.SpamFilter import SpamFilter
from src.models.ContactMessageEntity import ContactMessageEntity


class ContactPage(ControllerBase):
    def __init__(self):
        self.app_context = ApplicationContext()
        self.spam_filter = SpamFilter()  # Initialize SpamFilter

    def index(self):
        """ Render the contact page """
        return render_template('pages/general/contact.html')

    def __is_valid_name(self, name):
        """Validate the name. It should contain only letters and some special characters like spaces or hyphens."""
        pattern = r"^[a-zA-Z\s\-]+$"
        return re.match(pattern, name) is not None

    def __is_valid_email(self, email):
        """Validate the email format."""
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, email) is not None


    def post(self):
        # Get data from form
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')
        sent_on = datetime.datetime.now()

        # Validate name and email
        if not self.__is_valid_name(name):
            # Handle invalid name
            flash("Ongeldige naam opgegeven.", "error")
            return render_template('pages/general/contact.html')

        if not self.__is_valid_email(email):
            # Handle invalid email
            flash("Ongeldig e-mailadres.", "error")
            return redirect("/contact/")

        # Check if the message or email is spam
        if self.spam_filter.is_spam(message, email):
            # Handle spam (log it, redirect, flash message, etc.)
            flash('Uw bericht ziet eruit als spam. Wijzig en probeer het opnieuw.', 'error')
            return redirect("/contact/")

        # Create ContactFormEntity
        contact_form = ContactMessageEntity(0, email, name, message, sent_on)

        # Submit to database
        success = self.app_context.save_contact_message(contact_form)

        if success:
            flash("Je bericht is succesvol verzonden!", "success")
        else:
            flash("Er is een fout opgetreden bij het verzenden van uw bericht.", "error")

        return redirect('/contact')


if __name__ == "__main__":
    pass
