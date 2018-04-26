from flask import flash
from flask_admin.babel import gettext
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.sql.functions import current_user

from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models
from flask_login import current_user


class TicketView(UserRequiredMixin, ModelView):
    pass


class StatusView(UserRequiredMixin, ModelView):
    pass


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
admin.add_view(StatusView(models.Status, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
