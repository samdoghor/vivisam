"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""


# imports
import smtplib

import config
from flask import Flask, request
from flask_migrate import Migrate
from models import db
from flask_cors import CORS

# configurations

app = Flask(__name__)

app.config['SECRET_KEY'] = config.SECRET_KEY

app.config['SQLALCHEMY_DATABASE_URI'] = config.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_MODIFICATIONS_TRACKS'] = config.SQLALCHEMY_MODIFICATIONS_TRACKS  # noqa

db.init_app(app)
db.app = (app)
migrate = Migrate(app, db)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

env = config.ENV

# routes


@app.route('/')
def home():
    """ The funtion returns a 200 Ok to show app is running """
    return {
        'Status': '200 Ok',
        'Message': 'App is runnung',
    }


@app.route('/contact', methods=['POST', 'GET'])
def send_mail():
    """ This function sends mail in contact page for Vivirgros """
    try:
        data = request.get_json()

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
            Message: {project_details}
            """

        email = config.EMAIL_ADDRESS
        password = config.EMAIL_PASSWORD
        to = config.EMAIL_ADDRESS

        with smtplib.SMTP_SSL('mail.'+config.EMAIL_HOST, 465) as smtp:

            smtp.login(email, password)

            subject = mail_subject
            body = mail_message

            msg = "Subject: {}\n\n{}".format(subject, body)

            smtp.sendmail(email, to, msg)

        return print({
            'Message': 'Successfully Sent'
        })

    except Exception:
        return print({
            'Message': 'Failed to send'
        })

# @app.route('/blog')
# def blogHome():
#     return 'About'


if env:
    if __name__ == '__main__':
        app.run()
