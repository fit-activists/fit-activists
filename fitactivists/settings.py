# Standard libs
import os

class Config(object):
    SECRET_KEY = os.environ['SECRET_KEY']
    APP_DIR = os.path.abspath(os.path.dirname(__file__)) # This directory
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))

class ProdConfig(Config):
    ENV = 'prod'
    DEBUG = False

    # Database settings
    FIT_ACTIVISTS_DB_HOST = os.environ['FIT_ACTIVISTS_DB_HOST']
    FIT_ACTIVISTS_DB_NAME = os.environ['FIT_ACTIVISTS_DB_NAME']
    FIT_ACTIVISTS_DB_USER = os.environ['FIT_ACTIVISTS_DB_USER']
    FIT_ACTIVISTS_DB_PASSWORD = os.environ['FIT_ACTIVISTS_DB_PASSWORD']

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True

    # Database settings
    FIT_ACTIVISTS_DB_HOST = os.environ['FIT_ACTIVISTS_DB_HOST']
    FIT_ACTIVISTS_DB_NAME = os.environ['FIT_ACTIVISTS_DB_NAME']
    FIT_ACTIVISTS_DB_USER = os.environ['FIT_ACTIVISTS_DB_USER']
    FIT_ACTIVISTS_DB_PASSWORD = os.environ['FIT_ACTIVISTS_DB_PASSWORD']

