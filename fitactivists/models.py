# Standard libs
import datetime

# Third party libs
from flask.ext.login import UserMixin
import pymongo

# Our libs
from .database import DataStore

class MongoRecord(object):
    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = {}

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def update(self, updated_data):
        self.data.update(updated_data)

class User(MongoRecord, UserMixin):
    @classmethod
    def get_by_id(cls, _id):
        user_data = DataStore.db.users.find_one({'_id': _id})
        if user_data:
            return User(user_data)
        return None

    def get_id(self):
        return unicode(self['_id'])

    def verify_password(self, password):
        return True

