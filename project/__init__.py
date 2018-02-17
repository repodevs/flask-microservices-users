import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt


# instance the extensions
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)

    # enable CORS
    CORS(app)

    # set configuration
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    # setup extensions
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # registers blueprints
    from project.api.users import users_blueprint
    from project.api.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(users_blueprint)

    return app


