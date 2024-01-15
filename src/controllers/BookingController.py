""" Index Controller
"""
import json
from datetime import datetime, timedelta

import flask_login
# needed imports
from flask import render_template, request, redirect
from flask_login import current_user

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BookingEntity import BookingEntity
from src.models.UsersEntity import UsersEntity


class BookingPage(ControllerBase):
    """BookingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    @RouteMethods(["Get", "Post"])
    def book(self, accommodation_id):
        """ Endpoint for getting the index page
        """

        if not current_user.is_authenticated:
            return redirect(f"/login")

        applicationContext = ApplicationContext()

        if request.method == 'GET':
            data = applicationContext.Get(AccommodationEntity(), condition=f"id = {accommodation_id}")

            if len(data) != 1:
                return render_template("pages/error.html"), 500

            booked = applicationContext.Get(BookingEntity(), condition=f"accommodation_id = {accommodation_id}")

            booked_dates = []

            for booking in booked:
                booked_dates.append({
                    "start_date": str(booking.start_date),
                    "end_date": str(booking.end_date)
                })

            # return rendered html
            return render_template("pages/booking.html", accomondation=data[0],
                                   booked_dates_str=json.dumps(booked_dates))

        elif request.method == 'POST':
            date_format = "%Y-%m-%d"
            check_in_date_str = request.form.get('checkindate')
            check_out_date_str = request.form.get('checkoutdate')

            if not (check_in_date_str and check_out_date_str):
                return render_template("pages/error.html"), 500

            user = applicationContext.First(UsersEntity(), condition=f"email = '{flask_login.current_user.email}'")

            if user is None:
                return render_template("pages/error.html"), 500

            check_in_date = datetime.strptime(check_in_date_str, date_format)
            check_out_date = datetime.strptime(check_out_date_str, date_format)

            day_difference = (check_out_date - check_in_date).days + 1

            booking_count = int(day_difference // 7)

            last_start_date = check_in_date

            for booking_number in range(booking_count):
                if booking_number > 0:
                    last_start_date = last_start_date + timedelta(
                        days=7)

                booking = BookingEntity()
                booking.accommodation_id = accommodation_id
                booking.booking_date = datetime.now()
                booking.start_date = last_start_date
                booking.end_date = check_out_date if booking_number == booking_count - 1 else booking.start_date + timedelta(
                    days=7)
                booking.user_id = user.id
                booking.SetCreationDate()
                applicationContext.Add(booking)

            return redirect(f"/booking/thankyou/{accommodation_id}")

    def thankyou(self, accommodation_id):
        return redirect("pages/thank-you.html")


if __name__ == "__main__":
    pass
