from flask_admin.contrib.sqla import ModelView

from mg_incident import db, admin
from mg_incident.ticket import models


class TicketView(ModelView):
    pass


class StatusView(ModelView):
    pass


class TicketStatusView(ModelView):
    form_columns = ('ticket', 'status', 'description', 'created_by', )


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(StatusView(models.Status, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
