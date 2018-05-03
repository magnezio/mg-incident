from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError
from mg_incident import admin, db
from mg_incident.auth import AdminRequiredMixin
from mg_incident.models import AppRole, AppUser


class AppUserView(AdminRequiredMixin, ModelView):
    column_list = [
        'username', 'email', 'active', 'last_login_at', 'login_count',
    ]
    column_searchable_list = ['username', 'email', ]
    column_filters = ['active', 'roles', ]
    form_columns = ['username', 'email', 'active', 'password', 'roles', ]


class AppRoleView(AdminRequiredMixin, ModelView):
    column_list = ['name', 'description', ]
    column_searchable_list = ['name', ]
    form_excluded_columns = ['is_predefined', ]

    def on_model_delete(self, model):
        if model.is_predefined:
            raise ValidationError('Predefined role can not be deleted.')

    def on_model_change(self, form, model, is_created):
        if not is_created:
            if model.is_predefined:
                raise ValidationError('Predefined role can not be changed.')


admin.add_views(
    AppRoleView(AppRole, db.session),
    AppUserView(AppUser, db.session)
)
