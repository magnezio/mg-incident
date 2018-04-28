from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

from mg_incident import auth

db = SQLAlchemy()
mail = Mail()
admin = Admin(name='MG Incidents', url='/', template_mode='bootstrap3', base_template='base.html')
migrate = Migrate()


from mg_incident import models
from mg_incident import admin_views

def create_app(config_name='development'):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object('config.default')
    config_obj_name = "config.{}".format(config_name)
    # TODO: ImportError
    app.config.from_object(config_obj_name)
    db.init_app(app)
    mail.init_app(app)
    auth.do_security(app, db, models.AppUser, models.AppRole)
    migrate.init_app(app, db)
    admin.init_app(app)

    return app
