import os
from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow.exceptions import ValidationError
from flask_login import LoginManager


db = SQLAlchemy()
ma = Marshmallow()
lm = LoginManager()

def create_app():
    # Create the flask app object
    app = Flask(__name__)

    app.config.from_object("config.app_config")

    db.init_app(app)
    ma.init_app(app)
    lm.init_app(app)

    from commands import db_commands
    app.register_blueprint(db_commands)

    # Then we can register our routes  
    from controllers import registerable_controllers
    for controller in registerable_controllers:
        app.register_blueprint(controller)

    @app.errorhandler(ValidationError)
    def handle_bad_request(error):
        return (jsonify(error.messages), 400)

    return app