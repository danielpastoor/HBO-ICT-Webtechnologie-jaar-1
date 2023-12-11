""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class PricingPage(ControllerBase):
    """PricingPage controller for showing the Contact page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        # return rendered html
        return render_template("pages/pricing.html")

if __name__ == "__main__":
    pass
