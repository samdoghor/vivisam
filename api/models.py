"""
This Module defines the models of the backend for Vivirgros and Samuel Doghor
Website
"""


from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

# db initialisation

db = SQLAlchemy()


class AuthorModel(db.Model):
    """ Author Model """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), unique=True, nullable=False)
    profile_picture = db.Column(db.String(), nullable=True)
    password = db.Column(db.Integer(), nullable=False)

    # relationships

    blogs = db.relationship("BlogModel", backref="authors", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class BlogModel(db.Model):
    """ Blog Model """
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    feature_image = db.Column(db.String(), nullable=False)

    # foreign_keys

    author_id = db.Column(db.Integer, db.ForeignKey(
        'authors.id'), nullable=False, unique=True)

    # relationships

    blog_contents = db.relationship(
        "BlogContentModel", backref="blogs", lazy=True)
    blog_images = db.relationship(
        "BlogImageModel", backref="blogs", lazy=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class BlogContentModel(db.Model):
    """ Blog Content Model """
    __tablename__ = "blog_contents"

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(), nullable=False)

    # foreign_keys

    blog_id = db.Column(db.Integer, db.ForeignKey(
        'blogs.id'), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class BlogImageModel(db.Model):
    """ Blog Image Model """
    __tablename__ = "blog_images"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(), nullable=False)

    # foreign_keys

    blod_id = db.Column(db.Integer, db.ForeignKey(
        'blogs.id'), nullable=False, unique=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class EmailListModel(db.Model):
    """ Email List Model """
    __tablename__ = "email_lists"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(), nullable=True)
    customer_name = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), nullable=False)
    phone_number = db.Column(db.String(), nullable=False)
    is_vivirgros = db.Column(db.Boolean, nullable=False, default=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
