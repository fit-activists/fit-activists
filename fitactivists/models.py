# Standard libs
import datetime
import uuid

# Third party libs
import bcrypt
from flask.ext.login import UserMixin
import pymongo

# Our libs
from .database import DataStore

class MongoRecord(object):
    COLLECTION = ''

    @classmethod
    def get_by_id(cls, _id):
        if not cls.COLLECTION:
            raise Exception('COLLECTION not set')
        data = DataStore.db[cls.COLLECTION].find_one({'_id': _id})
        if data:
            return cls(data)
        return None

    def __init__(self, data=None):
        if data:
            self.data = data
        else:
            self.data = {}

    def __getitem__(self, name):
        return self.data[name]

    def __setitem__(self, name, value):
        self.data[name] = value

    def create(self):
        self['_id'] = uuid.uuid4().hex[:10]
        self['created'] = datetime.datetime.utcnow()
        _id = DataStore.db[self.__class__.COLLECTION].insert(self.data)

    def update(self, updated_data):
        self.data.update(updated_data)

class User(MongoRecord, UserMixin):
    COLLECTION = 'users'
    REQUIRED_FIELDS = [
        'email',
        'password',
        'first_name',
        'last_name',
        'date_of_birth',
        'company_name',
        'team_name',
    ]

    def get_id(self):
        return unicode(self['_id'])

    def verify_password(self, password):
        return bcrypt.hashpw(str(password), str(self['password'])) == self['password']

    def is_valid(self):
        for field in self.__class__.REQUIRED_FIELDS:
            if not self.data.get(field):
                return False

        if '@' not in self.data.get('email', ''):
            return False

        return True

    def create(self):
        self['_id'] = self['email']
        self['password'] = bcrypt.hashpw(str(self['password']), bcrypt.gensalt())
        self['created'] = datetime.datetime.utcnow()

        # Retrieve the user's company from the given company name
        # Create the company record if it doesn't exist
        company = Company.get_by_name(self['company_name'])
        if not company:
            company_data = {
                'name': self['company_name'],
            }
            company = Company(company_data)
            company.create()

        # Store the company ID in the user record
        self['company_id'] = company['_id']

        # Retrieve the user's team from the given team name
        # Create the team record if it doesn't exist
        team = Team.get_by_name(self['team_name'], company['_id'])
        if not team:
            team_data = {
                'name':       self['team_name'],
                'company_id': self['company_id'],
            }
            team = Team(team_data)
            team.create()

        # Store the team ID in the user record
        self['team_id'] = team['_id']

        _id = DataStore.db[self.__class__.COLLECTION].insert(self.data)

class Company(MongoRecord):
    COLLECTION = 'companies'

    @classmethod
    def get_by_name(cls, name):
        normalized_name = cls.normalize_company_name(name)
        data = DataStore.db[cls.COLLECTION].find_one({'name': normalized_name})
        if data:
            return Company(data)
        return None

    @classmethod
    def normalize_company_name(cls, company_name):
        return company_name.strip().lower()

class Team(MongoRecord):
    COLLECTION = 'teams'

    @classmethod
    def get_by_name(cls, name, company_id):
        normalized_name = cls.normalize_team_name(name)
        data = DataStore.db[cls.COLLECTION].find_one({'name': normalized_name, 'company_id': company_id})
        if data:
            return Team(data)
        return None

    @classmethod
    def normalize_team_name(cls, team_name):
        return team_name.strip().lower()

