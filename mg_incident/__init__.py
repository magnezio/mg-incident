from flask import Flask
from flask_admin.menu import MenuLink
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

from mg_incident import auth

db = SQLAlchemy()
admin = Admin(name='MG Incidents', url='/', template_mode='bootstrap3', base_template='base.html')
migrate = Migrate()

from mg_incident.account import models as account_models
from mg_incident.ticket import models as ticket_models

from mg_incident.account import admin_views as account_admin_views
from mg_incident.ticket import admin_views as ticket_admin_views
from mg_incident.feedback import admin_views

admin.add_link(MenuLink(name='Google', category='Links', url='http://www.google.com/'))
admin.add_link(MenuLink(name='Mozilla', category='Links', url='http://mozilla.org/'))


def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    # app.config.from_pyfile('config.py')
    config_obj_name = "config.{}".format(config_name)
    # TODO: ImportError
    app.config.from_object(config_obj_name)
    db.init_app(app)
    auth.do_security(app, db, account_models.AppUser, account_models.AppRole)
    migrate.init_app(app, db)
    admin.init_app(app)

    return app
