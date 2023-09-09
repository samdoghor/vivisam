"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""


from flask import Flask
from .config import SECRET_KEY

# configurations


app = Flask(__name__)

app.config['SECRET_KEY'] = SECRET_KEY


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


if __name__ == "__main__":
    app.run()
