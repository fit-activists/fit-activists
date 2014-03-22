# Standard libs
import datetime

# Third party libs
import bcrypt
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
        return bcrypt.hashpw(str(password), str(self['password'])) == self['password']

    def is_valid(self):
        if '@' not in self.data.get('email', ''):
            return False

        return True

    def create(self):
        self['_id'] = self['email']
        self['password'] = bcrypt.hashpw(str(self['password']), bcrypt.gensalt())
        self['created'] = datetime.datetime.utcnow()
        _id = DataStore.db.users.insert(self.data)

