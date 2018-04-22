from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# from flask_security import Security, SQLAlchemyUserDatastore

from flask_admin import Admin


db = SQLAlchemy()
admin = Admin(name='MG Incidents', url='/')
migrate = Migrate()


from mg_incident.account import models as account_models
from mg_incident.ticket import models as ticket_models

# user_datastore = SQLAlchemyUserDatastore(db, account_models.AppUser, account_models.AppRole)
# security = Security(datastore=user_datastore)

from mg_incident.account import admin_views as account_admin_views
from mg_incident.ticket import admin_views as ticket_admin_views


def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.default')
    app.config.from_pyfile('config.py')
    config_obj_name = "config.{}".format(config_name)
    # TODO: ImportError
    app.config.from_object(config_obj_name)

    db.init_app(app)
    # security.init_app(app)
    migrate.init_app(app, db)
    admin.init_app(app)

    return app
