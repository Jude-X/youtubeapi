import os
from dotenv import load_dotenv


class Config(object):
    DEBUG = False
    TESTING = False
    MONGODB_SETTINGS = {
        'db':'youtubeapi',
        'host': 'localhost',
        'port': 27017
    }
    
class DevelopmentConfig(Config):
    ENV = "development"
    SECRET_KEY = "judex"
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False