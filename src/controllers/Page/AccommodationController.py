""" Accommodation Controller
"""
# needed imports
from flask import render_template, request

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.AccommodationEntity import AccommodationEntity


class AccommodationController(ControllerBase):
    """PricingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def __init__(self):
        self.app_context = ApplicationContext()

    def get(self):
        """ Endpoint for getting the accommodation page
        """
        search = request.args.get("search")
        check_in_date = request.args.get("start_date")
        check_out_date = request.args.get("end_date")
        condition = None
        join = None
        column = "*"

        # create join if there is a filter
        if check_in_date and check_out_date:
            join = """
            LEFT JOIN booking ON accommodation.id = booking.accommodation_id
               AND (
                   booking.start_date <= '{}'
                   AND booking.end_date >= '{}'
               )
            """.format(check_out_date, check_in_date)
            column = "accommodation.*"

            condition = "booking.accommodation_id IS NULL"

        # create condition if there is a filter
        if search:
            column_search_key = "accommodation.name" if join else "name"

            if condition is None:
                condition = "{} LIKE '%{}%'".format(column_search_key, search)
            else:
                condition += " AND {} LIKE '%{}%'".format(column_search_key, search)

        # SELECT * FROM accommodation
        data = self.app_context.Get(AccommodationEntity(), column, condition, join)

        # return rendered html
        return render_template("pages/general/accommodation/accommodation-overview.html", accommodations=data,
                               found_items=len(data))

    def accommodation(self, accommodation_id):
        """ Endpoint for getting the accommodation detail page with id accommodation_id """

        data = self.app_context.Get(AccommodationEntity(), condition=f"id = {accommodation_id}")

        if len(data) != 1:
            return "There went something wrong", 500

        # list of all accommodations for the slider
        accommodations = self.app_context.Get(AccommodationEntity())

        # return rendered html
        return render_template("pages/general/accommodation/accommodation-detail.html", accommodation=data[0],
                               accommodations=accommodations,
                               found_items=len(accommodations))


if __name__ == "__main__":
    pass
