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
    DB_HOST = os.environ['DB_HOST']
    DB_NAME = os.environ['DB_NAME']
    DB_USER = os.environ['DB_USER']
    DB_PASSWORD = os.environ['DB_PASSWORD']

class DevConfig(Config):
    ENV = 'dev'
    DEBUG = True

    # Database settings
    DB_HOST = 'localhost:27017'
    DB_NAME = 'fit_activists'

