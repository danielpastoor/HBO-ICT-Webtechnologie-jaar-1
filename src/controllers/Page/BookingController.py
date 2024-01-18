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
from src.models.Enums.PaymentStatus import PaymentStatus
from src.models.PaymentEntity import PaymentEntity
from src.models.UsersEntity import UsersEntity


class BookingPage(ControllerBase):
    """BookingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    @RouteMethods(["Get", "Post"])
    def book(self, accommodation_id):
        """ Endpoint for getting the general page
        """

        if not current_user.is_authenticated:
            return redirect("/authentication/login")

        applicationContext = ApplicationContext()

        if request.method == 'GET':
            data = applicationContext.Get(AccommodationEntity(), condition=f"id = {accommodation_id}")

            if len(data) != 1:
                return render_template("pages/error/error.html"), 500

            booked = applicationContext.Get(BookingEntity(), condition=f"accommodation_id = {accommodation_id}")

            booked_dates = []

            for booking in booked:
                booked_dates.append({
                    "start_date": str(booking.start_date),
                    "end_date": str(booking.end_date)
                })

            # return rendered html
            return render_template("pages/general/booking/../../templates/pages/general/booking.html", accommodation=data[0],
                                   booked_dates_str=json.dumps(booked_dates))

        elif request.method == 'POST':
            accommodation = applicationContext.First(AccommodationEntity(), condition=f"id = {accommodation_id}")

            if accommodation is None:
                return render_template("pages/error/error.html"), 500

            date_format = "%Y-%m-%d"
            check_in_date_str = request.form.get('start_date')
            check_out_date_str = request.form.get('end_date')

            if not (check_in_date_str and check_out_date_str):
                return render_template("pages/error/error.html"), 500

            user = applicationContext.First(UsersEntity(), condition=f"email = '{flask_login.current_user.email}'")

            if user is None:
                return render_template("pages/error/error.html"), 500

            check_in_date = datetime.strptime(check_in_date_str, date_format)
            check_out_date = datetime.strptime(check_out_date_str, date_format)

            day_difference = (check_out_date - check_in_date).days + 1

            booking_count = int(day_difference // 7)

            last_start_date = check_in_date

            payment = PaymentEntity()
            payment.price = accommodation.price * day_difference
            payment.status = PaymentStatus.PENDING
            payment.SetCreationDate()
            # Create payment row
            payment.id = applicationContext.Add(payment)

            if payment.id is None:
                return render_template("pages/error/error.html"), 500

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
                booking.payment_id = payment.id
                booking.SetCreationDate()
                applicationContext.Add(booking)

            return redirect(self.__create_payment_url(payment.price, payment.id))

    def thankyou(self):
        return render_template("pages/general/thank-you.html")

    def __create_payment_url(self, amount, id):
        url_payment = f"http://localhost:8081/booking/payment/{id}/{PaymentStatus.COMPLETED}"
        url_success = f"http://localhost:8081/booking/payment/{id}/{PaymentStatus.COMPLETED}"
        url_pending = f"http://localhost:8081/booking/payment/{id}/{PaymentStatus.PENDING}"
        url_failure = f"http://localhost:8081/booking/payment/{id}/{PaymentStatus.ERROR}"

        return f'https://www.ideal-checkout.nl/demo/idealcheckout-betaalformulier/idealcheckout/checkout.php?amount={amount}&url_payment={url_payment}&url_success={url_success}&url_pending={url_pending}&url_failure={url_failure}'

    def payment(self, payment_id, payment_status):
        applicationContext = ApplicationContext()

        payment = applicationContext.First(PaymentEntity(), "*", condition=f"id = {payment_id}")

        if payment is None:
            return render_template("pages/error/error.html"), 500

        applicationContext.Update(PaymentEntity(), {
            "status": payment_status
        }, payment.id)

        return redirect("/booking/thankyou")


if __name__ == "__main__":
    pass
