"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""


from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

# configurations


app = Flask(__name__)

db = SQLAlchemy()

db.init_app(app)
db.app = (app)
migrate = Migrate(app, db)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


if __name__ == "__main__":
    app.run()
