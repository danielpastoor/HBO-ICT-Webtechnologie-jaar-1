""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase


class IndexController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """
        # return renderd html
        return render_template("pages/index.html")


if __name__ == "__main__":
    pass
