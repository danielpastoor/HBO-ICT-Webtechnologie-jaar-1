""" In this file are the routes defined
"""

from flask import Flask

from src.controllers.IndexController import IndexController


def routes(app: Flask):
    """Routes function so we can define the routes here
    """
    # Add controllers
    IndexController.register(app, "/")


if __name__ == "__main__":
    pass
