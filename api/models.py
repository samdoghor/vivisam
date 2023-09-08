"""
This Module defines the models of the backend for Vivirgros and Samuel Doghor
Website
"""


from flask_sqlalchemy import SQLAlchemy

# db initialisation

db = SQLAlchemy()


class Author(db.Model):
    """ Author Model """
    __tablename__ = "authors"

    id = db.Column(db.Integer, primary_key=True)
