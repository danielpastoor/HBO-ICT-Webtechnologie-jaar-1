""" Index Controller
"""
import json
from datetime import datetime

# needed imports
from flask import render_template, request
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
        applicationContext = ApplicationContext()

        if request.method == 'GET':
            data = applicationContext.Get(AccommodationEntity(), condition= f"id = {accommodation_id}")

            if len(data) != 1:
                return render_template("pages/error.html"), 500

            booked = applicationContext.Get(BookingEntity(), condition=f"accommodation_id = {accommodation_id}")

            booked_dates = []

            for booking in booked:
                booked_dates.append({
                    "start_date": str(booking.start_date),
                    "end_date": str(booking.end_date)
                })

            print(booked_dates)
            print(json.dumps(booked_dates))


            # return rendered html
            return render_template("pages/booking.html", accomondation=data[0], booked_dates_str=json.dumps(booked_dates))

        elif request.method == 'POST':
            bookingEntity = BookingEntity()

            bookingEntity.accommodation_id = accommodation_id
            bookingEntity.booking_date = datetime.now()
            bookingEntity.start_date = request.form.get('checkindate')
            bookingEntity.end_date = request.form.get('checkoutdate')
            bookingEntity.SetCreationDate()

            email = request.form.get('email')

            users = applicationContext.Get(UsersEntity(), condition=f"email = '{email}'")

            user = UsersEntity()

            if len(users) > 0:
                user = users[0]
            else:
                user.username = request.form.get('username')
                user.email = request.form.get('email')
                user.postalcode = request.form.get('postalcode')
                user.address = request.form.get('street')
                user.housenumber = request.form.get('housenumber')
                user.city = request.form.get('city')
                user.creditcard = request.form.get('creditcard')
                user.password = None

                applicationContext.Add(user)

                users = applicationContext.Get(UsersEntity(), condition=f"email = '{email}'")

                if len(users) > 0:
                    user = users[0]
                else:
                    return render_template("pages/error.html"), 500

            bookingEntity.user_id = user.id

            applicationContext.Add(bookingEntity)

            return render_template("pages/thank-you.html")


if __name__ == "__main__":
    pass
