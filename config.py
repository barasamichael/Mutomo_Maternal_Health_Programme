import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or \
            'Fighting poverty, ignorance and diseases'
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = os.environ.get('MAIL_PORT', '587')
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true')\
            .lower() in ['True', 'on', 1]
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    FLASKY_ADMIN_EMAIL = os.environ.get('FLASKY_ADMIN_EMAIL')\
            or 'mmhcpuser001@gmail.com'
    FLASKY_MAIL_SUBJECT_PREFIX = os.environ.get('FLASKY_MAIL_SUBJECT_PREFIX')\
            or '[Mutomo Maternal Health Care Programme]'
    FLASKY_MAIL_SENDER = os.environ.get('FLASKY_MAIL_SENDER')\
            or 'Mutomo Maternal Health Programme Admin <mmhcporg@gmail.com>'
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ORGANISATION_NAME = os.environ.get('ORGANISATION_NAME') or 'Mutomo Maternal Health Programme'
    
    FLASKY_POSTS_PER_PAGE = os.environ.get('FLASKY_POSTS_PER_PAGE') or 30

    PATIENT_UPLOAD_PATH = os.path.join(basedir + '/app/static/profiles/patients')
    HEALTH_PRACTITIONER_UPLOAD_PATH = os.path.join(basedir + '/app/static/profiles/practitioners')
    HEALTH_CENTER_UPLOAD_PATH = os.path.join(basedir + '/app/static/profiles/health_centers')
    CENTER_DEPARTMENT_UPLOAD_PATH = os.path.join(basedir + '/app/static/profiles/health_departments')
    
    UPLOAD_EXTENSIONS = ['.jpg', '.gif', '.jpeg', '.png']


@staticmethod
def init_app(app):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data-dev-sqlite')
    

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite://'


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') \
            or 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

config = {
        'development' : DevelopmentConfig,
        'testing' : TestingConfig,
        'production' : ProductionConfig,
        'default' : DevelopmentConfig
        }





