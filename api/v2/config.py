''' configaration file for various environments such as production or testing'''
import os

class BaseConfig():
    '''parent class subclassed by all other environ ment classes'''
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.urandom(24)


class Development(BaseConfig):
    '''class contains all configs relatedd to development enviroment'''
    DEBUG = True
    TESTING = True
    os.environ['DB_NAME'] = 'sol'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = ''
    os.environ['DB_HOST'] = 'localhost'


class Test(BaseConfig):
    '''the class is used to run tests'''
    TESTING = True
    DEBUG = True
    """os.environ['DB_NAME'] = 'soltests'
    os.environ['DB_USER'] = 'postgres'
    os.environ['DB_PASSWORD'] = 'andela2018'
    os.environ['DB_HOST'] = 'localhost'"""


class Production(BaseConfig):
    '''production configarations'''
    TESTING = False


CONFIG = {
    'development': Development,
    'testing': Test,
    'production': Production
}
