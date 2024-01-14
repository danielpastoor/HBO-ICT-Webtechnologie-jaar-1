""" Index Controller
"""
import datetime
import re

# needed imports
from flask import render_template, request, flash, redirect
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.data.ContactFormEntity import ContactFormEntity
from src.data.SpamFilter import SpamFilter


class ContactPage(ControllerBase):
    def __init__(self):
        self.app_context = ApplicationContext()
        self.spam_filter = SpamFilter()  # Initialize SpamFilter

    def index(self):
        """ Render the contact page """
        return render_template('pages/contact.html')

    def is_valid_name(self, name):
        """Validate the name. It should contain only letters and some special characters like spaces or hyphens."""
        pattern = r"^[a-zA-Z\s\-]+$"
        return re.match(pattern, name) is not None

    def is_valid_email(self, email):
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
        if not self.is_valid_name(name):
            # Handle invalid name
            flash("Invalid name provided.", "error")
            return render_template('pages/contact.html')

        if not self.is_valid_email(email):
            # Handle invalid email
            flash("Invalid email address.", "error")
            return render_template('pages/contact.html')

        # Check if the message or email is spam
        if self.spam_filter.is_spam(message, email):
            # Handle spam (log it, redirect, flash message, etc.)
            flash('Your message looks like spam. Please modify and try again.', 'error')
            return render_template('pages/contact.html')

        # Create ContactFormEntity
        contact_form_entity = ContactFormEntity(name, email, message, sent_on)

        # Submit to database
        success = self.app_context.submit_contact_form(contact_form_entity)

        if success:
            flash("Your message has been sent successfully!", "success")
        else:
            flash("There was an error sending your message.", "error")

        return redirect('/contact')


if __name__ == "__main__":
    pass
