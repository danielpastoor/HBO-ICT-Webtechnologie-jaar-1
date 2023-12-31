""" In this file are the routes defined
"""

from flask import Flask

from src.controllers.AuthenticationController import LoginPage, RegisterPage
from src.controllers.BookingController import BookingPage
from src.controllers.ContactController import ContactPage
from src.controllers.FAQController import FaqPage
from src.controllers.IndexController import IndexController
from src.controllers.PricingController import PricingPage


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.register(app, "/")
    ContactPage.register(app, "/contact")
    BookingPage.register(app, "/booking")
    PricingPage.register(app, "/pricing")
    FaqPage.register(app, "/faqs")
    LoginPage.register(app, "/login")
    RegisterPage.register(app, "/register")


if __name__ == "__main__":
    pass
