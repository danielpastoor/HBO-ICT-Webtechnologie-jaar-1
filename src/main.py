"""In deze file worden de scripts gerund"""
import os
from sys import argv
from flask import Flask
from datetime import timedelta
from flask_login import LoginManager
from werkzeug.middleware.profiler import ProfilerMiddleware

from src.data.ApplicationContext import ApplicationContext
from src.routes.route import routes
from src.settings import init_env

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'default_secret_key')

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Adjust if necessary

@login_manager.user_loader
def load_user(username):
    return ApplicationContext().get_user_by_username(username)

# load config
init_env()

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

    app.run(debug=True, port=8081)
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days=14)


if __name__ == '__main__':
    pass
