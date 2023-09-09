"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""
import smtplib

from flask import Flask, jsonify, request
from flask_cors import CORS

from .config import EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, SECRET_KEY

# configurations


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY

CORS(app, resources={
     r"/contact": {"origins": ["https://vivirgros.com"]}})

# routes


@app.route('/')
def home():
    return 'Hello, World!'


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
            to = EMAIL_ADDRESS

            with smtplib.SMTP_SSL('mail.'+EMAIL_HOST, 465) as smtp:

                smtp.login(email, password)

                subject = mail_subject
                body = mail_message

                msg = f"Subject: {subject}\n\n{body}"

                smtp.sendmail(email, to, msg)

            return jsonify({
                'Message': 'Sent Successfully',
            }), 200

        except Exception:
            print(Exception)
            # Return an error response as JSON
            return jsonify({'Message': 'Failed to send'}), 500

    else:
        print(Exception)
        # Return an error response as JSON
        return jsonify({'Message': 'Failed to send'}), 500


if __name__ == "__main__":
    app.run()
