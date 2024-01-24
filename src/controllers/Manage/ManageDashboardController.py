""" Index Controller
"""
# needed imports
from flask import render_template, flash
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase
from src.data.ApplicationContext import ApplicationContext


class AdminDashboardController(ControllerBase):

    @login_required
    def index(self):
        app_context = ApplicationContext()
        dashboard_data = app_context.get_dashboard_data()

        return render_template("pages/manage/manage.html",
                               **dashboard_data)


if __name__ == "__main__":
    pass
