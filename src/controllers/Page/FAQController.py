""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class FaqPage(ControllerBase):
    """FaqPage controller for showing the Faq page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the general page
        """
        # return rendered html
        return render_template("pages/general/faq.html")

if __name__ == "__main__":
    pass
