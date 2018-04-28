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
    form_columns = ['username', 'email', 'active', 'tickets', 'tickets_assigned_by', 'tickets_assigned_to',
                    'tickets_statuses', 'last_login_at', 'current_login_at', 'last_login_ip', 'current_login_ip',
                    'login_count', 'confirmed_at']
    form_widget_args = {
        'last_login_ip': {
            'disabled': True
        },
        'current_login_ip': {
            'disabled': True
        },
        'login_count': {
            'disabled': True
        },
        'confirmed_at': {
            'disabled': True
        },
        'current_login_at': {
            'disabled': True
        },
        'last_login_at': {
            'disabled': True
        }
    }


class AppRole(AdminRequiredMixin, ModelView):
    column_list = ['name', 'description', ]
    column_searchable_list = ['name', ]


admin.add_view(AppUser(models.AppUser, db.session))
admin.add_view(AppRole(models.AppRole, db.session))
