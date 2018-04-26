from flask_admin.contrib.sqla import ModelView

from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models


class TicketView(UserRequiredMixin, ModelView):
    pass


class StatusView(UserRequiredMixin, ModelView):
    form_excluded_columns = ('predefined',)


class TicketStatusView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'status', 'description', 'created_by',)


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(StatusView(models.Status, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
