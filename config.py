import os


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:root@localhost:5432/flaskapp"
    SQLALCHEMY_TRACK_MODIFICATIONS = False