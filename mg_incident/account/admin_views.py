from flask_admin.contrib.sqla import ModelView

from mg_incident import db
from mg_incident import admin

from . import models


class AppUser(ModelView):
    column_list = ['username', 'email', 'active', 'last_login_at', \
        'last_login_ip', 'login_count', ]
    column_searchable_list = ['username', 'email', ]
    column_filters = ['active', ]


class AppRole(ModelView):
    column_list = ['name', 'description', ]
    column_searchable_list = ['name', ]


admin.add_view(AppUser(models.AppUser, db.session))
admin.add_view(AppRole(models.AppRole, db.session))