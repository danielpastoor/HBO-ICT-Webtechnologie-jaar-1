""" In this file are the routes defined
"""

from flask import Flask

from src.controllers.DashboardController import DashboardController
from src.controllers.AuthenticationController import LoginPage, RegisterPage, LogoutPage, ResetPasswordController
from src.controllers.BookingController import BookingPage
from src.controllers.ContactController import ContactPage
from src.controllers.FAQController import FaqPage
from src.controllers.IndexController import IndexController
from src.controllers.AccommodationController import AccommodationController


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.register(app, "/")
    ContactPage.register(app, "/contact")
    BookingPage.register(app, "/booking")
    AccommodationController.register(app, "/accommodation")
    FaqPage.register(app, "/faqs")
    LoginPage.register(app, "/login")
    RegisterPage.register(app, "/register")
    LogoutPage.register(app, "/logout")
    ResetPasswordController.register(app, "/reset-password")

    # Dashboard
    DashboardController.register(app, "/dashboard")


if __name__ == "__main__":
    pass
