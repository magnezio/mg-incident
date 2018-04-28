from flask_admin.contrib.sqla import ModelView
from mg_incident import admin, db
from mg_incident.auth import AdminRequiredMixin
from mg_incident.models import AppRole, AppUser


class AppUserView(AdminRequiredMixin, ModelView):
    column_list = ['username', 'email', 'active', 'last_login_at', \
        'last_login_ip', 'login_count', ]
    column_searchable_list = ['username', 'email', ]
    column_filters = ['active', 'roles', ]
    form_excluded_columns = ['password', ]


class AppRoleView(AdminRequiredMixin, ModelView):
    column_list = ['name', 'description', ]
    column_searchable_list = ['name', ]


admin.add_views(
    AppRoleView(AppRole, db.session),
    AppUserView(AppUser, db.session)
)