""" In this file are the routes defined
"""

from flask import Flask, render_template

from src.controllers.Authentication.AuthenticationController import AuthenticationController
from src.controllers.Dashboard.MyBookingController import MyBookingController
from src.controllers.Dashboard.ProfileController import ProfileController
from src.controllers.Manage.ManageAccomodationsController import ManageAccommodationController
from src.controllers.Manage.ManageBookingController import ManageBookingController
from src.controllers.Manage.ManageDashboardController import AdminDashboardController
from src.controllers.Manage.ManageSupportController import ManageSupportController
from src.controllers.Manage.ManageUserController import ManageUserController
from src.controllers.Page.AccommodationController import AccommodationController
from src.controllers.Page.BookingController import BookingPage
from src.controllers.Page.ChatController import ChatController
from src.controllers.Page.ContactController import ContactPage
from src.controllers.Page.FAQController import FaqPage
from src.controllers.Page.GeneralConditionController import GeneralConditionController
from src.controllers.Page.IndexController import IndexController


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.registerRoutes(app, "/")
    ContactPage.registerRoutes(app, "/contact")
    BookingPage.registerRoutes(app, "/booking")
    AccommodationController.registerRoutes(app, "/accommodation")
    FaqPage.registerRoutes(app, "/faqs")
    GeneralConditionController.registerRoutes(app, "/general-condition")

    # authentication
    AuthenticationController.registerRoutes(app, "/authentication")

    # Profile Page
    ProfileController.registerRoutes(app, "/dashboard/settings")

    # MyBooking's Page
    MyBookingController.registerRoutes(app, "/dashboard/my-booking")

    # Chat Popup
    ChatController.registerRoutes(app, "/dashboard/save-chat")

    # --- Mange

    # All-Booking
    ManageBookingController.registerRoutes(app, "/manage/bookings")

    # Add User & Remove Controller
    ManageUserController.registerRoutes(app, "/manage/users")

    # Manage Accommodation Controller
    ManageAccommodationController.registerRoutes(app, "/manage/accommodations")

    # Manage Support requests from support button
    ManageSupportController.registerRoutes(app, "/manage/support-chat")

    # AdminDash Controller
    AdminDashboardController.registerRoutes(app, "/manage")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("pages/error/error.html")


if __name__ == "__main__":
    pass
