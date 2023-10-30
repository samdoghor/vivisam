"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""
import smtplib

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_migrate import Migrate

from .config import (EMAIL_ADDRESS, EMAIL_HOST, EMAIL_PASSWORD, SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MODIFICATIONS_TRACKS)  # noqa
from .errors import (BadRequest, DataNotFound, TooManyRequest,
                     Forbidden, Conflict, InternalServerError)

from .models import (db, EmailListModel, AuthorModel,
                     BlogModel, BlogContentModel, BlogImageModel)

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
                               "vivirgros.com", "http://localhost:5173",
                               "localhost:5173"]}})

# routes


@app.route('/')
def home():
    """ This function confirms the site is running """

    return jsonify({
        'code': 200,
        'message': 'The application is running'
    })


""" Authors """
# create new author


@app.route('/new_author', methods=['POST'])
def new_author(first_name, last_name, email_address, profile_picture, password):  # noqa
    """ This function defines a route to create a new author """

    try:
        authors = AuthorModel.query.filter_by(
            email_address=email_address).first()

        if not authors:
            new_author = AuthorModel(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                profile_picture=profile_picture
            )
            new_author.set_password(password)

            db.session.add(new_author)
            db.session.commit()

            return jsonify({
                'Message': 'Author Created Successfully',
            }), 200

        else:
            return jsonify({
                'Message': 'Author Already Exist'
            })

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# get one author


@app.route('/author/<int:id>', methods=['GET'])
def author(id):
    """ This function defines a route to display an author info """

    try:
        authors = AuthorModel.query.filter_by(id=id).first()

        if not authors:

            return jsonify({
                'Message': f'Author with id {id} was not found',
            }), 200

        else:
            data = {
                'id': authors.id,
                'first_name': authors.first_name,
                'last_name': authors.last_name,
                'email_address': authors.email_address,
                'profile_picture': authors.profile_picture
            }

            return jsonify({
                'Message': f'Author with id {id} was found',
                'Author': data
            })

    except DataNotFound as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# update one author

@app.route('/author/<int:id>', methods=['PUT'])
def update_author(id, first_name, last_name, email_address, profile_picture, password):  # noqa
    """ This function defines a route to update an existing author """

    try:
        author = AuthorModel.query.filter_by(id=id).first()

        if author:
            update_author = AuthorModel(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                profile_picture=profile_picture
            )
            update_author.set_password(password)

            db.session.commit()

            return jsonify({
                'Message': 'Author Updated Successfully',
            }), 200

        else:
            return jsonify({
                'Message': 'Author Update Failed'
            })

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# delete one author


@app.route('/author/<int:id>', methods=['DELETE'])
def delete_author(id):  # noqa
    """ This function defines a route to delte an author """

    try:
        authors = AuthorModel.query.filter_by(id=id).first()

        if not authors:

            return jsonify({
                'Message': f'Author with id {id} was not found',
            }), 200

        else:
            db.session.delete(authors)
            db.session.commit()

            return jsonify({
                'Message': f'Author with id {id} was found and was deleted',
            })

    except DataNotFound as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


""" Blogs """
# create new blog


@app.route('/new_blog', methods=['POST'])
def new_blog(id, title, feature_image, content):  # noqa
    """ This function defines a route to create a new blog """

    try:
        new_blog = BlogModel(
            title=title,
            feature_image=feature_image
        )
        db.session.add(new_blog)

        new_content = BlogContentModel(
            blog_id=BlogModel.query.filter_by(id=id).first(),
            content=content
        )
        db.session.add(new_content)

        new_image = BlogImageModel(
            blog_id=BlogModel.query.filter_by(id=id).first(),
            image=content
        )
        db.session.add(new_image)

        db.session.commit()

        return jsonify({
            'Message': 'Blog Created Successfully',
        }), 200

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# get one blog


@app.route('/blog/<int:id>', methods=['GET'])
def blog(id):
    """ This function defines a route to display a blog """

    try:
        authors = AuthorModel.query.filter_by(id=id).first()

        if not authors:

            return jsonify({
                'Message': f'Author with id {id} was not found',
            }), 200

        else:
            data = {
                'id': authors.id,
                'first_name': authors.first_name,
                'last_name': authors.last_name,
                'email_address': authors.email_address,
                'profile_picture': authors.profile_picture
            }

            return jsonify({
                'Message': f'Author with id {id} was found',
                'Author': data
            })

    except DataNotFound as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# update one blog

@app.route('/blog/<int:id>', methods=['PUT'])
def update_blog(id, first_name, last_name, email_address, profile_picture, password):  # noqa
    """ This function defines a route to update an existing blog """

    try:
        author = AuthorModel.query.filter_by(id=id).first()

        if author:
            update_author = AuthorModel(
                first_name=first_name,
                last_name=last_name,
                email_address=email_address,
                profile_picture=profile_picture
            )
            update_author.set_password(password)

            db.session.commit()

            return jsonify({
                'Message': 'Author Updated Successfully',
            }), 200

        else:
            return jsonify({
                'Message': 'Author Update Failed'
            })

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


# delete one blog


@app.route('/blog/<int:id>', methods=['DELETE'])
def deleteblog(id):  # noqa
    """ This function defines a route to delete a blog """

    try:
        authors = AuthorModel.query.filter_by(id=id).first()

        if not authors:

            return jsonify({
                'Message': f'Author with id {id} was not found',
            }), 200

        else:
            db.session.delete(authors)
            db.session.commit()

            return jsonify({
                'Message': f'Author with id {id} was found and was deleted',
            })

    except DataNotFound as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Forbidden as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except Conflict as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }

    except InternalServerError as e:
        return {
            'Code': e.code,
            'Type': e.type,
            'Message': e.message
        }


""" Contact """
# send a contact message to vivirgros and save details in contact list


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

            # add to customer list

            customer = EmailListModel.query.filter_by(
                email_address=email_address).first()

            if not customer:
                new_customer = EmailListModel(
                    company_name=company_name,
                    customer_name=your_name,
                    email_address=email_address,
                    phone_number=phone_number,
                )
                db.session.add(new_customer)
                db.session.commit()

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
