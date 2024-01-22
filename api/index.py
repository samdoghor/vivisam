"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""
import datetime
import smtplib

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_login import LoginManager, login_required, login_user, logout_user
from flask_migrate import Migrate

from .config import (EMAIL_ADDRESS, EMAIL_ADDRESS_SAMDOGHOR, EMAIL_HOST,
                     EMAIL_HOST_SAMDOGHOR, EMAIL_PASSWORD,
                     EMAIL_PASSWORD_SAMDOGHOR, SECRET_KEY,
                     SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MODIFICATIONS_TRACKS)
from .errors import (BadRequest, Conflict, DataNotFound, Forbidden,
                     InternalServerError, TooManyRequest)
from .models import (AuthorModel, BlogContentModel, BlogModel, EmailListModel,
                     db)

# configurations


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI  # noqa
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_MODIFICATIONS_TRACKS  # noqa
app.config['SECRET_KEY'] = SECRET_KEY

db.app = app
db.init_app(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)


allowed_origins = ["https://www.vivirgros.com",
                   "https://vivirgros.com",
                   "vivirgros.com",
                   "https://www.samdoghor.com",
                   "https://samdoghor.com",
                   "samdoghor.com"]

# allowed_origins = ["localhost:5173", "http://localhost:5173"]

CORS(app, resources={r"/*": {"origins": allowed_origins}})

# routes


@app.route('/')
def home():
    """ This function confirms the site is running """

    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    exact_date = datetime.date.today()

    return jsonify({
        'code': 200,
        'message': f'The application started running at {formatted_time} on {exact_date}'  # noqa
    })


""" Authors """
# create new author


@app.route('/new_author', methods=['POST'])
def new_author():  # noqa
    """ This function defines a route to create a new author """

    try:
        data = request.get_json()

        authors = AuthorModel.query.filter_by(
            email_address=data['email_address']).first()

        if 'email_address' in data == authors:
            return jsonify({
                'Message': 'Author Already Exist'
            })

        first_name = data['first_name']
        last_name = data['last_name']
        email_address = data['email_address']
        profile_picture = data['profile_picture']

        author = AuthorModel(first_name=first_name, last_name=last_name,
                             email_address=email_address,
                             profile_picture=profile_picture)

        author.set_password(data['password'])

        db.session.add(author)
        db.session.commit()

        return jsonify({
            'Message': 'Author Created Successfully',
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
@login_required
def update_author(id, first_name, last_name, email_address, profile_picture, password):  # noqa
    """ This function defines a route to update an existing author """

    try:
        author = AuthorModel.query.filter_by(id=id).first()

        if author:
            data = request.get_json()

            if 'first_name' in data:
                author.first_name = data['first_name']

            if 'last_name' in data:
                author.last_name = data['last_name']

            if 'email_address' in data:
                author.email_address = data['email_address']

            if 'profile_picture' in data:
                author.profile_picture = data['profile_picture']

            if 'password' in data:
                author.set_password(data['password'])

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
@login_required
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
@login_required
def new_blog():  # noqa
    """ This function defines a route to create a new blog """

    try:
        data = request.get_json()

        if 'title' and 'feature_image' not in data:
            return jsonify({
                'Message': 'Tile and Feature Image cannot be empty'
            })

        title = data['title']
        feature_image = data['feature_image']

        content = data['content']

        blog = BlogModel(title=title, feature_image=feature_image)
        db.session.add(blog)

        # TODO: Modify Blog Creation to Match Table

        blogContent = BlogContentModel(blog_id=blog.id, content=content)

        db.session.add(blogContent)
        db.session.commit()

        return jsonify({
            'Message': 'Author Created Successfully',
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
        blog = BlogModel.query.filter_by(id=id).first()

        if not blog:
            return jsonify({
                'Message': f'Blog with id {id} was not found',
            }), 200

        data = {
            'id': blog.id,
            'title': blog.title,
            'feature_image': blog.feature_image,
            'blog_contents': blog.blog_contents,
            'blog_images': blog.blog_images
        }

        return jsonify({
            'Message': f'Blog with id {id} was found',
            'Blog': data
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
@login_required
def update_blog(id):  # noqa
    """ This function defines a route to update an existing blog """

    try:
        blog = BlogModel.query.filter_by(id=id).first()

        if blog:
            data = request.get_json()

            if 'title' in data:
                blog.title = data['title']

            if 'feature_image' in data:
                blog.feature_image = data['feature_image']

            if 'content' in data:
                blog.content = data['content']

            if 'image' in data:
                blog.image = data['image']

            db.session.commit()

            return jsonify({
                'Message': 'Blog Updated Successfully',
            }), 200

        else:
            return jsonify({
                'Message': 'Blog Update Failed'
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
@login_required
def deleteblog(id):  # noqa
    """ This function defines a route to delete a blog """

    try:
        blogs = BlogModel.query.filter_by(id=id).first()

        if not blogs:

            return jsonify({
                'Message': f'Blog with id {id} was not found',
            }), 200

        else:
            db.session.delete(blogs)
            db.session.commit()

            return jsonify({
                'Message': f'Blog with id {id} was found and was deleted',
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


""" Other Logics """
# login an author


@app.route('/login', methods=['POST'])
def login_author():
    """ This function defines the login method """

    data = request.get_json()

    if data:
        try:
            author_email = AuthorModel.query.filter_by(
                email_address=data['email_address']).first()

            if author_email is not None and author_email.check_password(data['password']):  # noqa
                login_user(author_email)

                return jsonify({
                    'Message': 'Logged in Successfully',
                }), 200

        except BadRequest as error:
            return jsonify({
                'message': f"{error} occur. This is a bad request"
            }), 400

        except TooManyRequest as error:
            return jsonify({
                'message': f"{error} occur. There are too many request"
            }), 429


# logout an author


@app.route("/logout")
@login_required
def logout():
    try:
        logout_user()

        return jsonify({
            'Message': 'Logged out Successfully',
        }), 200

    except BadRequest as error:
        return jsonify({
            'message': f"{error} occur. This is a bad request"
        }), 400

    except TooManyRequest as error:
        return jsonify({
            'message': f"{error} occur. There are too many request"
        }), 429


""" Contact """
# send a contact message to vivirgros and save details in contact list


@app.route('/contact', methods=['POST'])
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

            # add to customer list

            try:

                customer = EmailListModel.query.filter_by(
                    email_address=email_address, is_vivirgros=True).first()

                if customer is None:
                    new_customer = EmailListModel(
                        company_name=company_name,
                        customer_name=your_name,
                        email_address=email_address,
                        phone_number=phone_number,
                    )
                    db.session.add(new_customer)
                    db.session.commit()

                    return jsonify({
                        'Message': 'Contact Saved Successfully',
                    }), 200
            except BadRequest as error:
                return jsonify({
                    'message': f"{error} occur. This is a bad request"
                }), 400

            except TooManyRequest as error:
                return jsonify({
                    'message': f"{error} occur. There are too many request"
                }), 429

            return jsonify({
                'Message': 'Message Sent and Contact Saved Successfully',
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


@app.route('/contact-samdoghor', methods=['POST'])
def send_mail_samdoghor():
    """ This function sends mail in contact page for Samuel, Doghor """

    data = request.get_json()

    if data:
        try:
            company_name = data["companyName"]
            your_name = data["yourName"]
            phone_number = data["phoneNumber"]
            email_address = data["emailAddress"]
            project_details = data["projectDetails"]

            mail_subject = "A Message from Samdoghor Contact Page"
            mail_message = f"""\
            This message is from Samdoghor Contact Page

            Message Details Below:

                Company Name: {company_name}

                Client Name: {your_name}

                Mobile Number: {phone_number}

                Email Address: {email_address}

                Message: {project_details}"""

            email = EMAIL_ADDRESS_SAMDOGHOR
            password = EMAIL_PASSWORD_SAMDOGHOR
            to_email = EMAIL_ADDRESS_SAMDOGHOR

            with smtplib.SMTP_SSL('mail.'+EMAIL_HOST_SAMDOGHOR, 465) as smtp:

                smtp.login(email, password)

                subject = mail_subject
                body = mail_message

                msg = f"Subject: {subject}\n\n{body}"

                smtp.sendmail(email, to_email, msg)

            return jsonify({
                'Message': 'Sent Successfully',
            }), 200

            # add to customer list

            try:

                customer = EmailListModel.query.filter_by(
                    email_address=data["emailAddress"],
                    is_vivirgros=False).first()

                if customer is None:
                    new_customer = EmailListModel(
                        company_name=data["companyName"],
                        customer_name=data["yourName"],
                        email_address=data["emailAddress"],
                        phone_number=data["phoneNumber"],
                        is_vivirgros=False
                    )
                    db.session.add(new_customer)
                    db.session.commit()

                    return jsonify({
                        'Message': 'Contact Saved Successfully',
                    }), 200
            except BadRequest as error:
                return jsonify({
                    'message': f"{error} occur. This is a bad request"
                }), 400

            except TooManyRequest as error:
                return jsonify({
                    'message': f"{error} occur. There are too many request"
                }), 429

            return jsonify({
                'Message': 'Message Sent and Contact Saved Successfully',
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
