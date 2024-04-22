from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager


# Defining the method to create and initialise Flask app


def create_app():
    app = Flask(__name__)
    app.static_folder = "assets"
    app.config["SECRET_KEY"] = "<SECRET KEY>"

    app.config["MONGODB_SETTINGS"] = {
        'db': 'SAMI_Hotel',
        'host': 'mongodb+srv://<username>:<password>@cluster0.nfr0aog.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
    }
    db = MongoEngine(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message = "Please log in to access this page!"

    return app, db, login_manager


# Calling the create_app method
app, db, login_manager = create_app()
