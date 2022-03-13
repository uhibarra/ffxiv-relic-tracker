import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))

load_dotenv(os.path.join(basedir, '.env'))

class Config():
    """
    Set Config variables for the app.
    Use environment variables where available. Otherwise, create the Config variable if not done already.

    """

    # Secret key -- needed for flask to run -- preventative measure against cookie tampering
    SECRET_KEY = os.environ.get('SECRET_KEY') or "You've committed the cardinal sin of boring me."

    # Access the PGAdmin4 Database URL
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEPLOY_DATABASE_URL') or "sqlite:///" + os.path.join(basedir, 'app.db')

    # Turn off messages for updates in sqlalchemy
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask App variable
    FLASK_APP = os.environ.get('FLASK_APP')

    # Flask Env variable
    FLASK_ENV = os.environ.get('FLASK_ENV')

