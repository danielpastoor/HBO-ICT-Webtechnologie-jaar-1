""" In this file are the routes defined
"""

from flask import Flask, render_template

from src.controllers.Dashboard.DashboardController import DashboardController
from src.controllers.Authentication.AuthenticationController import LoginPage, RegisterPage, LogoutPage, ResetPasswordController
from src.controllers.Page.BookingController import BookingPage
from src.controllers.Page.ContactController import ContactPage
from src.controllers.Page.FAQController import FaqPage
from src.controllers.Page.GeneralConditionController import GeneralConditionController
from src.controllers.Page.IndexController import IndexController
from src.controllers.Page.AccommodationController import AccommodationController
from src.controllers.Dashboard.MyBookingController import MyBookingController
from src.controllers.Page.ChatController import ChatController
from src.controllers.Manage.ManageBookingController import ManageBookingController
from src.controllers.Manage.ManageSupportController import ManageSupportController
from src.controllers.Manage.ManageUserController import ManageUserController
from src.controllers.Dashboard.ProfileController import ProfileController
from src.controllers.Manage.ManageAccomodationsController import ManageAccommodationController, AddAccommodationController
from src.controllers.Manage.ManageDashboardController import AdminDashboardController


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.register(app, "/")
    ContactPage.register(app, "/contact")
    BookingPage.register(app, "/booking")
    AccommodationController.register(app, "/accommodation")
    FaqPage.register(app, "/faqs")

    # authentication
    LoginPage.register(app, "/authentication/login")
    RegisterPage.register(app, "/authentication/register")
    LogoutPage.register(app, "/authentication/logout")
    ResetPasswordController.register(app, "/authentication/reset-password")

    # All-Booking
    DashboardController.register(app, "/dashboard/all-bookings")

    # MyBooking's Page
    MyBookingController.register(app, "/dashboard/my-booking")

    # Chat Popup
    ChatController.register(app, "/dashboard/save-chat")

    # Profile Page
    ProfileController.register(app, "/dashboard/settings")

    # Booking creation Admin page
    ManageBookingController.register(app, "/dashboard/create-booking")

    # Add User & Remove Controller
    ManageUserController.register(app, "/dashboard/submit-new-user")
    # UserRemovalController.register(app, "/dashboard/remove-user")

    # Edit User Controller
    # RegisterUserController.register(app, "/dashboard/edit-users")

    # Manage Accommodation Controller
    ManageAccommodationController.register(app, "/dashboard/manage-accommodations")
    AddAccommodationController.register(app, "/dashboard/add-accommodation")

    # Manage Support requests from support button
    ManageSupportController.register(app, "/dashboard/support-chat")

    # AdminDash Controller
    AdminDashboardController.register(app, "/dashboard")

    GeneralConditionController.register(app, "/general-condition")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("pages/error/error.html")


if __name__ == "__main__":
    pass
