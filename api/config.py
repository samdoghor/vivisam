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

POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_DATABASE = os.getenv('POSTGRES_DATABASE')


# Enable debug mode.

DEBUG = True

# Connect to the database

# SQLALCHEMY_DATABASE_URI = f'postgresql://{USER_NAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}'  # noqa
SQLALCHEMY_DATABASE_URI = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{PORT}/{POSTGRES_DATABASE}'  # noqa
SQLALCHEMY_MODIFICATIONS_TRACKS = False
