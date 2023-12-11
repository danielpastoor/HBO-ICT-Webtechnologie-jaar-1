""" Index Controller
"""
# needed imports
from flask import render_template
# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext
from src.models.BaseModel.TransientObject import TransientObject


class ExampleController(ControllerBase):
    """index controller for showing the home page

    Returns:
        _type_: page
    """

    # get
    def index(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        data = applicationContext.Get("table_name")

        print(data)

        # return rendered html
        return render_template("pages/index.html")

    # add
    def post(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        data = TransientObject()

        data.SetValue("hallojumbo", 60)

        applicationContext.Add("table_name", data)


        # return rendered html
        return render_template("pages/index.html")

    # put or update
    def put(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        data = TransientObject()

        data.SetValue("hallojumbo", 60)

        applicationContext.Update("table_name", data, 10)


        # return rendered html
        return render_template("pages/index.html")

    # delete
    def delete(self):
        """ Endpoint for getting the index page
        """

        applicationContext = ApplicationContext()

        applicationContext.Delete("table_name", 10)

        # return rendered html
        return render_template("pages/index.html")


if __name__ == "__main__":
    pass
