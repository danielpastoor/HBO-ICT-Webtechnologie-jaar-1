""" Book Controller
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
from src.models.Enums.PaymentStatus import PaymentStatus
from src.models.PaymentEntity import PaymentEntity
from src.models.UsersEntity import UsersEntity


class BookingPage(ControllerBase):
    """BookingPage controller for showing the booking page

    Returns:
        _type_: page
    """

    def __init__(self):
        self.app_context = ApplicationContext()

    @RouteMethods(["Get", "Post"])
    def book(self, accommodation_id):
        """ Endpoint for getting the book page
        """

        # check if user is authenticated
        if not current_user.is_authenticated:
            return redirect("/authentication")

        # get the accommodation
        accommodation = self.app_context.First(AccommodationEntity(), condition=f"id = {accommodation_id}")

        if accommodation is None:
            return redirect("/error")

        if request.method == 'GET':
            # get booking so we can disable some dates
            booked = self.app_context.Get(BookingEntity(), column="start_date, end_date", condition=f"accommodation_id = {accommodation_id}")

            booked_dates = []

            # get all start and end dates
            for booking in booked:
                booked_dates.append({
                    "start_date": str(booking.start_date),
                    "end_date": str(booking.end_date)
                })

            # return rendered html
            return render_template("pages/general/booking.html", accommodation=accommodation,
                                   booked_dates_str=json.dumps(booked_dates))

        elif request.method == 'POST':
            date_format = "%Y-%m-%d"
            check_in_date_str = request.form.get('start_date')
            check_out_date_str = request.form.get('end_date')
            specialRequests = request.form.get('specialRequests')

            # check if there are booking dates
            if not (check_in_date_str and check_out_date_str):
                return redirect("/error")

            # get user data
            user = self.app_context.First(UsersEntity(), condition=f"email = '{flask_login.current_user.email}'")

            if user is None:
                return redirect("/error")

            # get correct date format
            check_in_date = datetime.strptime(check_in_date_str, date_format)
            check_out_date = datetime.strptime(check_out_date_str, date_format)

            # get day difference
            day_difference = (check_out_date - check_in_date).days + 1

            # get the total weeks
            booking_count = int(day_difference // 7)

            last_start_date = check_in_date

            # create a payment entity so users can pay
            payment = PaymentEntity()
            payment.price = accommodation.price * day_difference
            payment.status = PaymentStatus.PENDING
            payment.SetCreationDate()
            # Create payment row
            payment.id = self.app_context.Add(payment)


            if payment.id is None:
                return redirect("/error")

            # Loop count of bookings
            for booking_number in range(booking_count):
                # check if it is the first booking
                if booking_number > 0:
                    last_start_date = last_start_date + timedelta(
                        days=7)

                # create booking entity
                booking = BookingEntity()
                booking.accommodation_id = accommodation_id
                booking.booking_date = datetime.now()
                booking.start_date = last_start_date
                booking.end_date = check_out_date if booking_number == booking_count - 1 else booking.start_date + timedelta(
                    days=7)
                booking.user_id = user.id
                booking.payment_id = payment.id
                booking.SetCreationDate()
                booking.special_requests = specialRequests
                # add booking to database
                self.app_context.Add(booking)

            # redirect to payment url
            return redirect(self.__create_payment_url(payment.price, payment.id))

    def thankyou(self):
        # thank you page
        return render_template("pages/general/thank-you.html")

    def __create_payment_url(self, amount, id):
        # generate payment url

        # geenrate urls
        url_payment = f"{request.base_url}booking/payment/{id}/{PaymentStatus.COMPLETED.value}"
        url_success = f"{request.base_url}booking/payment/{id}/{PaymentStatus.COMPLETED.value}"
        url_pending = f"{request.base_url}booking/payment/{id}/{PaymentStatus.PENDING.value}"
        url_failure = f"{request.base_url}booking/payment/{id}/{PaymentStatus.ERROR.value}"

        return f'https://www.ideal-checkout.nl/demo/idealcheckout-betaalformulier/idealcheckout/checkout.php?amount={amount}&url_payment={url_payment}&url_success={url_success}&url_pending={url_pending}&url_failure={url_failure}'

    def payment(self, payment_id, payment_status):
        # get payment
        payment = self.app_context.First(PaymentEntity(), "*", condition=f"id = {payment_id}")

        # check if payment exist
        if payment is None:
            return redirect("/error")

        # Update payment
        self.app_context.Update(PaymentEntity(), {
            "status": payment_status
        }, payment.id)

        # return thank you
        return redirect("/booking/thankyou")


if __name__ == "__main__":
    pass
