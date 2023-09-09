"""
This Module defines the routes of the backend for Vivirgros and Samuel Doghor
Website
"""


from flask import Flask

# configurations


app = Flask(__name__)


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/about')
def about():
    return 'About'


if __name__ == "__main__":
    app.run()
