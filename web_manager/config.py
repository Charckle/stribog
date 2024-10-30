import sys
from os import environ 


class Config(object):
    # environmental variables are set in .env, for development purpoises
    DEBUG = False
    TESTING = False
    SECRET_KEY = environ.get('SWM_SECRET_KEY', "B\xb2?.\xdf\x9f\xa7m\xf8\x8a%,\xf7\xc4\xfa\x91")
    
    JWT_SECRET_KEY = environ.get('SWM_JWT_SECRET_KEY', "sdf34tasdft34")
    
    APP_NAME = environ.get('SWM_APP_NAME', "Stribog Manager")
    
    ADMIN_USERNAME = environ.get('SWM_ADMIN_USERNAME', "admin")
    # SHA512
    # banana
    ADMIN_PASS_HASH = environ.get('SWM_ADMIN_PASS_HASH', "$6$rounds=656000$Q3Z3OlpOU0VOPRCd$LIRME01nvrON4QNQX1tTYAcBVRhujpG2GNdzCJHmvSJDMN4ZJDYkm5r4qb9WGXW9cPoDCxWnXL43tqU6IezTw0")
    
    SESSION_COOKIE_SECURE = True
    
    APP_LOGGING = environ.get('SWM_APP_LOGGING', "INFO")    
    

    # Application threads. A common general assumption is
    # using 2 per available processor cores - to handle
    # incoming requests using one and performing background
    # operations using the other.
    THREADS_PER_PAGE = 2
    
    # Enable protection agains *Cross-site Request Forgery (CSRF)*
    # CSRF_ENABLED = environ.get('CSRF_ENABLED', False)
    

    
class ProductionConfig(Config):
    TESTING = False

class DevelopmentConfig(Config):
    DEBUG = True

    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    TESTING = True

    SESSION_COOKIE_SECURE = False