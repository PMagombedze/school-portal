class Config(object):
    DEBUG = True
    TESTING = False
    SECRET_KEY = '1234567890'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    