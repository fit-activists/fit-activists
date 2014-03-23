# Third party libs
from flask import Flask
from flask_sslify import SSLify

# Our libs
from .database import DataStore
from .extensions import login_manager
from .models import User
from .blueprints import root
from .blueprints import api

def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_extensions(app)
    register_blueprints(app)

    return app

def register_extensions(app):
    login_manager.init_app(app)
    login_manager.login_view = 'root.login'

    DataStore.init(app.config)

    sslify = SSLify(app)

def register_blueprints(app):
    app.register_blueprint(root.blueprint)
    app.register_blueprint(api.blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

