import os
import db_config as cfg
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'test'

    DB_HOST = cfg.mysql['host']
    DB_USER = cfg.mysql['user']
    DB_PASSWORD = cfg.mysql['pw']
    DB_NAME = cfg.mysql['db']
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://' + DB_USER + ':@' + DB_HOST + '/' + DB_NAME
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    POSTS_PER_PAGE = 2 

