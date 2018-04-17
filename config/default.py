import os


DEBUG = False

BABEL_DEFAULT_LOCALE = os.environ.get('MGI_LOCALE', 'ru')
BABEL_DEFAULT_TIMEZONE = os.environ.get('MGI_TIMEZONE', 'UTC')

DB_USER = os.environ.get('MGI_DB_USER', 'mgincident_webapp')
DB_PASSWORD = os.environ.get('MGI_DB_PASSWORD')
DB_HOST = os.environ.get('MGI_DB_HOST', 'localhost')
DB_NAME = os.environ.get('MGI_DB_NAME', 'mgincident')

SQLALCHEMY_DATABASE_URI = 'postgresql://{}:{}@{}/{}'.format(
    DB_USER, DB_PASSWORD, DB_HOST, DB_NAME
)
