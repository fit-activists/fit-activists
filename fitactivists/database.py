# Third party libs
import pymongo

class DataStore(object):
    db = None

    @classmethod
    def init(cls, app_config):
        mongo_client = pymongo.MongoClient(app_config['DB_HOST'])
        cls.db = mongo_client[app_config['DB_NAME']]

        if app_config.get('DB_USER') and app_config.get('DB_PASSWORD'):
            cls.db.authenticate(app_config['DB_USER'], app_config['DB_PASSWORD'])

