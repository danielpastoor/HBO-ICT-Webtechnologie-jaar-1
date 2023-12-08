"""In deze file worden de scripts gerund"""

from sys import argv
from flask import Flask
from werkzeug.middleware.profiler import ProfilerMiddleware
from src.routes.route import routes

app = Flask(__name__)

# for enabling profiler
if len(argv) > 1 and "--profile" in argv:
    app.wsgi_app = ProfilerMiddleware(app.wsgi_app, profile_dir="cprofiling")

routes(app)


def run():
    """
    In this function we'll collect all the other
    functions. When this function is ran, the website
    will show up.
    """

    app.run(debug=True, port=8080)


if __name__ == '__main__':
    pass
