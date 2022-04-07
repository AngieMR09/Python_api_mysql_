from distutils.command.config import config 
from distutils.debug import DEBUG

class DevelopmentConfig():
    DEBUG = True
    MYSQL_HOST = 'localhost'
    MYSQL_USER = 'root'
    MYSQL_PASSWORD = '12345'
    MYSQL_DB = 'api_flask'

config={
    'development': DevelopmentConfig
}