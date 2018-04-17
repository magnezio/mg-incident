from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from flask_babelex import Babel, gettext

from flask_admin import Admin

import os


app = Flask(__name__, instance_relative_config=True)

# Load the default configuration
app.config.from_object('config.default')

# Load the configuration from the instance folder
app.config.from_pyfile('config.py')

# Load the file specified by the MGI_CONFIG_FILE environment variable
# Variables defined here will override those in the default configuration
config_name = "config.{}".format(
    os.environ.get('MGI_CONFIG_FILE', 'development')
)
# TODO: ImportError
app.config.from_object(config_name)


db = SQLAlchemy(app)
migrate = Migrate(app, db)
babel = Babel(app)

admin_name = gettext('Incident Management')
admin = Admin(app, name=admin_name, url='/')
