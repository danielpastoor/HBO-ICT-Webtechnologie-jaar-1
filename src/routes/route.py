""" In this file are the routes defined
"""

from flask import Flask, render_template

from src.controllers.DashboardController import DashboardController
from src.controllers.AuthenticationController import LoginPage, RegisterPage, LogoutPage, ResetPasswordController
from src.controllers.BookingController import BookingPage
from src.controllers.ContactController import ContactPage
from src.controllers.FAQController import FaqPage
from src.controllers.IndexController import IndexController
from src.controllers.AccommodationController import AccommodationController
from src.controllers.MyBookingController import MyBookingController
from src.controllers.ChatController import ChatController
from src.controllers.ProfileController import ProfileController
from src.controllers.CreateBookingController import CreateBookingController
from src.controllers.AddUserController import AddUserController
from src.controllers.RegisterUserController import RegisterUserController
from src.controllers.AddAccommodationController import AddAccommodationController
from src.controllers.ManageAccomodationsController import ManageAccommodationController
from src.controllers.SupportUserController import SupportUserController
from src.controllers.AdminDashboardController import AdminDashboardController


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

    # All-Booking
    DashboardController.register(app, "/dashboard/all-bookings")

    # MyBooking's Page
    MyBookingController.register(app, "/dashboard/my-booking")

    # Chat Popup
    ChatController.register(app, "/dashboard/save-chat")

    # Profile Page
    ProfileController.register(app, "/dashboard/settings")

    # Booking creation Admin page
    CreateBookingController.register(app, "/dashboard/create-booking")

    # Add User Controller
    AddUserController.register(app, "/dashboard/submit-new-user")

    # Edit User Controller
    RegisterUserController.register(app, "/dashboard/edit-users")

    # Add Accommodation Controller
    AddAccommodationController.register(app, "/dashboard/add-accommodation")

    # Manage Accommodation Controller
    ManageAccommodationController.register(app, "/dashboard/manage-accommodations")

    # Manage Support requests from support button
    SupportUserController.register(app, "/dashboard/support-chat")

    # AdminDash Controller
    AdminDashboardController.register(app, "/dashboard")

    @app.errorhandler(404)
    def not_found(e):
        return render_template("pages/error/error.html")


if __name__ == "__main__":
    pass
