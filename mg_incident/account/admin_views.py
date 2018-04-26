from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError

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
    column_list = ['name', 'description', 'predefined']
    column_searchable_list = ['name', ]
    form_excluded_columns = ['predefined']

    def on_model_delete(self, model):
        if model.predefined:
            raise ValidationError('Predefined role can not be deleted.')

    def on_model_change(self, form, model, is_created):
        if model.predefined:
            raise ValidationError('Predefined role can not be changed.')

    def delete_model(self, model):
        """
            Delete model.

            :param model:
                Model to delete
        """
        try:
            self.on_model_delete(model)
            if not model.predefined:
                self.session.flush()
                self.session.delete(model)
                self.session.commit()
            if model.predefined:
                return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True


admin.add_view(AppUser(models.AppUser, db.session))
admin.add_view(AppRole(models.AppRole, db.session))
