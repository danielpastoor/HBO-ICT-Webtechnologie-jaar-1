""" Manage Controller
"""
# needed imports
from flask import render_template
from flask_login import login_required

# own imports
from src.controllers.Base.ControllerBase import ControllerBase, check_is_admin
from src.data.ApplicationContext import ApplicationContext


class AdminDashboardController(ControllerBase):

    def __init__(self):
        self.app_context = ApplicationContext()

    @login_required
    @check_is_admin
    def index(self):
        # get dashboard data
        dashboard_data = self.app_context.get_dashboard_data()

        # show manage dashboard pages
        return render_template("pages/manage/manage.html",
                               **dashboard_data)


if __name__ == "__main__":
    pass
