# Third party libs
import pymongo

class DataStore(object):
    db = None

    @classmethod
    def init(cls, app_config):
        mongo_client = pymongo.MongoClient(app_config['FIT_ACTIVISTS_DB_HOST'])
        cls.db = mongo_client[app_config['FIT_ACTIVISTS_DB_NAME']]

        if app_config.get('FIT_ACTIVISTS_DB_USER') and app_config.get('FIT_ACTIVISTS_DB_PASSWORD'):
            cls.db.authenticate(app_config['FIT_ACTIVISTS_DB_USER'], app_config['FIT_ACTIVISTS_DB_PASSWORD'])

