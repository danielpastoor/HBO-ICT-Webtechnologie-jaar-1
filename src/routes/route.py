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
    DashboardController.register(app, "/all-bookings")

    # MyBooking's Page
    MyBookingController.register(app, "/my-booking")

    # Chat Popup
    ChatController.register(app, "/save-chat")

    # Profile Page
    ProfileController.register(app, "/settings")

    # Booking creation Admin page
    CreateBookingController.register(app, "/create-booking")

    # Add User Controller
    AddUserController.register(app, "/submit-new-user")

    # Edit User Controller
    RegisterUserController.register(app, "/edit-users")

    # Add Accommodation Controller
    AddAccommodationController.register(app, "/add-accommodation")

    # Manage Accommodation Controller
    ManageAccommodationController.register(app, "/manage-accommodations")

    # Manage Support requests from support button
    SupportUserController.register(app, "/support-chat")

    # AdminDash Controller
    AdminDashboardController.register(app, "/dashboard")



if __name__ == "__main__":
    pass
