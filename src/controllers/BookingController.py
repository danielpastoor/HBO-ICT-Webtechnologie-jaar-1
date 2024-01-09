""" Index Controller
"""
from datetime import datetime

# needed imports
from flask import render_template, request
# own imports
from src.controllers.Base.ControllerBase import ControllerBase, RouteMethods
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity
from src.models.BookingEntity import BookingEntity
from src.models.UserEntity import UserEntity


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
                return "There went something wrong", 500

            # return rendered html
            return render_template("pages/booking.html", booking=data[0])

        elif request.method == 'POST':
            bookingEntity = BookingEntity()

            bookingEntity.accommodation_id = accommodation_id
            bookingEntity.booking_date = datetime.now()
            bookingEntity.start_date = request.form.get('checkindate')
            bookingEntity.end_date = request.form.get('checkoutdate')
            bookingEntity.SetCreationDate()

            email = request.form.get('email')

            users = applicationContext.Get(UserEntity(), condition=f"email = {email}")

            user = UserEntity()

            if len(users) > 0:
                user = users[0]
            else:
                user.username = request.form.get('username')
                user.email = request.form.get('email')
                user.postalcode = request.form.get('postalcode')
                user.adress = request.form.get('street')
                user.housenumber = request.form.get('housenumber')
                user.city = request.form.get('city')
                user.creditcard = request.form.get('creditcard')

                applicationContext.Add(user)

                users = applicationContext.Get(UserEntity(), condition=f"email = {email}")

                if len(users) > 0:
                    user = users[0]
                else:
                    return render_template("pages/error.html")

            bookingEntity.user_id = user.id

            applicationContext.Add(bookingEntity)

            return render_template("pages/thank-you.html")


if __name__ == "__main__":
    pass
