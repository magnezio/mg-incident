from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError

from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models


class TicketView(UserRequiredMixin, ModelView):
    form_columns = ('name', 'description', 'parent', 'children', 'ticket_statuses',
                    'created_at', 'created_by', 'assigned_by', 'assigned_to')

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


class StatusView(UserRequiredMixin, ModelView):
    pass


class TicketStatusView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'status', 'description', 'created_by',)


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(StatusView(models.Status, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
