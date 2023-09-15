"""
This Module defines the models of the backend for Vivirgros and Samuel Doghor
Website
"""


from datetime import datetime

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# db initialisation

db = SQLAlchemy()


def db_setup(app):
    """ This function defines database setup and binds it to the app """

    app.config.from_object('config')
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    return db


class Author(db.Model):
    """ Author Model """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(), nullable=False)
    last_name = db.Column(db.String(), nullable=False)
    email_address = db.Column(db.String(), unique=True, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
