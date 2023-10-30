"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""
import smtplib

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from .config import (EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MODIFICATIONS_TRACKS)  # noqa
from .errors import BadRequest, DataNotFound, TooManyRequest

from .models import db

# configurations


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # noqa
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_MODIFICATIONS_TRACKS  # noqa
app.config['SECRET_KEY'] = SECRET_KEY

db.app = app
db.init_app(app)
migrate = Migrate(app, db)

CORS(app, resources={
     r"/contact": {"origins": ["https://www.vivirgros.com",
                               "https://vivirgros.com",
                               "vivirgros.com"]}})

# routes


@app.route('/')
def home():
    """ This function confirms the site is running """

    return jsonify({
        'code': 200,
        'message': 'The application is running'
    })


@app.route('/contact', methods=['GET', 'POST'])
def send_mail():
    """ This function sends mail in contact page for Vivirgros """

    data = request.get_json()

    if data:
        try:
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
            to_email = EMAIL_ADDRESS

            with smtplib.SMTP_SSL('mail.'+EMAIL_HOST, 465) as smtp:

                smtp.login(email, password)

                subject = mail_subject
                body = mail_message

                msg = f"Subject: {subject}\n\n{body}"

                smtp.sendmail(email, to_email, msg)

            return jsonify({
                'Message': 'Sent Successfully',
            }), 200

        except BadRequest as error:
            return jsonify({
                'message': f"{error} occur. This is a bad request"
            }), 400

        except TooManyRequest as error:
            return jsonify({
                'message': f"{error} occur. There are too many request"
            }), 429

    else:
        return jsonify({
            'message': f"{DataNotFound} occur. Data not found"
        }), 404


if __name__ == "__main__":
    app.run()
