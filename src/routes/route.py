""" In this file are the routes defined
"""

from flask import Flask

from src.controllers.IndexController import IndexController, ContactPage, BookingPage, PricingPage, FaqPage


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.register(app, "/")
    ContactPage.register(app, "/contact")
    BookingPage.register(app, "/booking")
    PricingPage.register(app, "/pricing")
    FaqPage.register(app, "/faqs")


if __name__ == "__main__":
    pass
