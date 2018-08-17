''' configaration file for various environments such as production or testing'''


class BaseConfig():
    '''parent class subclassed by all other environ ment classes'''
    DEBUG = False
    TESTING = False


class Development(BaseConfig):
    '''class contains all configs relatedd to development enviroment'''
    DEBUG = True
    TESTING = True


class Test(BaseConfig):
    '''the class is used to run tests'''
    TESTING = True
    DEBUG = True


class Production(BaseConfig):
    '''production configarations'''
    TESTING = False


CONFIG = {
    'development': Development,
    'testing': Test,
    'production': Production
}
