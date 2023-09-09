"""
This Module defines the configuration of the backend for Vivirgros and Samuel
Doghor Website
"""


# imports

import os

from dotenv import load_dotenv

# configurations

load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
USER_NAME = os.getenv('USER_NAME')
PASSWORD = os.getenv('PASSWORD')
DB_NAME = os.getenv('DB_NAME')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
ENV = os.getenv('ENV')

EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
EMAIL_HOST = os.getenv('EMAIL_HOST')
EMAIL_PORT = os.getenv('EMAIL_PORT')


# Enable debug mode.

DEBUG = True

# Connect to the database

SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'  # noqa
SQLALCHEMY_MODIFICATIONS_TRACKS = False
