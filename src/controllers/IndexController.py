""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject


class IndexController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    def index(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        data = applicationContext.Get("table_name")

        print(data)

        # return rendered html
        return render_template("pages/index.html")

if __name__ == "__main__":
    pass
