from flask_admin.contrib.sqla import ModelView

from mg_incident import db
from mg_incident import admin

from . import models


class AppUser(ModelView):
    pass


admin.add_view(AppUser(models.AppUser, db.session))