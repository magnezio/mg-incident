from flask_admin.contrib.sqla import ModelView

from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models


class TicketView(UserRequiredMixin, ModelView):
    pass


class TicketStatusView(UserRequiredMixin, ModelView):
    column_list = ('name', 'description', 'user_roles')
    column_searchable_list = ('name', 'user_roles.name')
    column_filters = ('name', 'user_roles.name')


class TicketStatusTrackingView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'ticket_status', 'description', 'created_by', 'created_at',)
    column_filters = ('ticket.name', 'ticket_status.name', 'description', 'created_by.username',)
    column_searchable_list = ('ticket.id', 'ticket_status.name', 'description',)


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
admin.add_view(TicketStatusTrackingView(models.TicketStatusTracking, db.session))
