"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""


import os
# imports
import smtplib

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# from .config import (EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, ENV,
#                      SECRET_KEY, SQLALCHEMY_DATABASE_URI,
#                      SQLALCHEMY_MODIFICATIONS_TRACKS)
# from .models import db

# configurations

app = Flask(__name__)

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

app.config['SECRET_KEY'] = SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_MODIFICATIONS_TRACKS'] = SQLALCHEMY_MODIFICATIONS_TRACKS  # noqa

db = SQLAlchemy()

db.init_app(app)
db.app = (app)
migrate = Migrate(app, db)

CORS(app, resources={
     r"/contact": {"origins": ["http://localhost:5173",
                               "https://vivirgros.com"]}})

env = ENV

# models


class Author(db.Model):
    """ Author Model """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)


# routes


@app.route('/')
def home():
    """ The funtion returns a 200 Ok to show app is running """
    return jsonify({
        'Status': '200 Ok',
        'Message': 'App is runnung',
    })


@app.route('/contact', methods=['GET', 'POST'])
def send_mail():
    """ This function sends mail in contact page for Vivirgros """

    data = request.get_json()

    if data:
        company_name = data["companyName"]
        your_name = data["yourName"]
        phone_number = data["phoneNumber"]
        email_address = data["emailAddress"]
        project_details = data["projectDetails"]

        mail_subject = "A Message from Vivirgros Contact Page"
        mail_message = f"""\
        This message is from Vivirgros Contact Page

        Message Details Below:

            Company Name: {company_name}

            Client Name: {your_name}

            Mobile Number: {phone_number}

            Email Address: {email_address}

            Message: {project_details}"""

        email = EMAIL_ADDRESS
        password = EMAIL_PASSWORD
        to = EMAIL_ADDRESS

        with smtplib.SMTP_SSL('mail.'+EMAIL_HOST, 465) as smtp:

            smtp.login(email, password)

            subject = mail_subject
            body = mail_message

            msg = f"Subject: {subject}\n\n{body}"

            smtp.sendmail(email, to, msg)

        return jsonify({
            'Message': 'Sent Successfully',
            # 'Data': mail_message,
            # 'Server': {
            #     'Email': email,
            #     'password': password,
            #     'to': to
            # }
        })

    else:
        print(Exception)
        # Return an error response as JSON
        return jsonify({'Message': 'Failed to send'}), 500

# @app.route('/blog')
# def blogHome():
#     return 'About'


# if env:
#     if __name__ == '__main__':
#         app.run()
