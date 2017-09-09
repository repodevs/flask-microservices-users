import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy


# db instance
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # set configuration
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # setup extensions
    db.init_app(app)

    # registers blueprints
    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app


