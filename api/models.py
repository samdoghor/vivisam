"""
This Module defines the models of the backend for Vivirgros and Samuel Doghor
Website
"""


from datetime import datetime

# from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# db initialisation

db = SQLAlchemy()


class Author(db.Model):
    """ Author Model """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), unique=True, nullable=False)
    profile_picture = db.Column(db.String(), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Blog(db.Model):
    """ Blog Model """
    __tablename__ = "blogs"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(), nullable=False)
    content = db.Column(db.String(), nullable=False)
    thumbnail = db.Column(db.String())

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Blog_Image(db.Model):
    """ Blog Image Model """
    __tablename__ = "blog_images"

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Email_list(db.Model):
    """ Email List Model """
    __tablename__ = "email_lists"

    id = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(), nullable=False)
    customer_name = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    phone_name = db.Column(db.String(), nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
