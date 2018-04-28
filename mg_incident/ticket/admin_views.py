from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError
from sqlalchemy.sql.functions import current_user
from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models
from flask_login import current_user


class TicketView(UserRequiredMixin, ModelView):
    form_columns = ('name', 'description', 'parent', 'children', 'ticket_statuses',
                    'created_at', 'created_by', 'assigned_by', 'assigned_to')
    column_filters = ('created_by.username', 'assigned_by.username', 'assigned_to.username',)

    def on_model_delete(self, model):
        if model.children:
            raise ValidationError("You can't deleting tickets that have child records")

    def delete_model(self, model):
        """
            Delete model.
            :param model:
                Model to delete
        """
        try:
            self.on_model_delete(model)
            if not model.children:
                self.session.flush()
                self.session.delete(model)
                self.session.commit()
            if model.children:
                return False
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

            self.session.rollback()

            return False
        else:
            self.after_model_delete(model)

        return True

# =======

class TicketStatusTrackingView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'ticket_status', 'description', 'created_by', 'created_at')
    
# =======

class StatusView(UserRequiredMixin, ModelView):
    form_excluded_columns = ('predefined',)

    def on_model_delete(self, model):
        if model.predefined:
            raise ValidationError('Predefined status can not be deleted.')

    def on_model_change(self, form, model, is_created):
        if model.predefined:
            raise ValidationError('Predefined status can not be changed.')

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


class TicketStatusView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'status', 'description',)

    def create_model(self, form):
        try:
            model = self.model()
            model.created_by_id = current_user.id
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except Exception as ex:
            if not self.handle_view_exception(ex):
                flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')

            self.session.rollback()

            return False
        else:
            self.after_model_change(form, model, True)

        return model


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
admin.add_view(TicketStatusTrackingView(models.TicketStatusTracking, db.session))
