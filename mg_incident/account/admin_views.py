from flask_admin.contrib.sqla import ModelView

from mg_incident import db
from mg_incident import admin

from mg_incident.auth import AdminRequiredMixin
from . import models


class AppUser(AdminRequiredMixin, ModelView):
    column_list = ['username', 'email', 'active', 'last_login_at',
                   'last_login_ip', 'login_count', ]
    column_searchable_list = ['username', 'email', ]
    column_filters = ['active', 'roles', ]
    form_excluded_columns = ['password', ]


class AppRole(AdminRequiredMixin, ModelView):
    column_list = ['name', 'description', ]
    column_searchable_list = ['name', ]


class AppRoleStatus(AdminRequiredMixin, ModelView):
    pass


admin.add_view(AppUser(models.AppUser, db.session))
admin.add_view(AppRole(models.AppRole, db.session))
admin.add_view(AppRoleStatus(models.AppRoleStatus, db.session))
