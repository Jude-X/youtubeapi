from flask import Flask
from flask_cors import CORS
from flask_restplus import Api
from youtubeapi.config import DevelopmentConfig


def create_app():
    from youtubeapi.api_namespace import api_namespace
    application = Flask(__name__)
    CORS(application)
    application.config.from_object(config.DevelopmentConfig)
    api = Api(application, doc='/test', version='0.1',title='Youtube Backend Api', description='A CRUD API')
    from youtubeapi.db import db
    db.init_app(application)
    application.db = db

    api.add_namespace(api_namespace)
    
    return application


application = create_app()

