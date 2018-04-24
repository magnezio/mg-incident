from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.ticket import models


class FilterCreatedBy(BaseSQLAFilter):
    def __init__(self, column, name, options=None, data_type=None):
        def get_users():
            users = []
            try:
                # TODO Problem are here.
                # "No application found. Either work inside a view function or push an application context."
                # I tried use it with current_app.app_context but unsuccessfully
                # users = models.Ticket.query.all()
                pass
            except Exception as e:
                raise e
            return [(user.id, str(user)) for user in users]

        super(FilterCreatedBy, self).__init__(column, name, get_users(), data_type)

    def apply(self, query, value, alias=None):
        return query.filter(self.column == value)

    def operation(self):
        from flask_admin.babel import gettext
        return gettext('equals')


class TicketView(UserRequiredMixin, ModelView):
    # TODO Options should be generated automatically, but now its problem to make query to db from current view
    column_filters = [
        FilterCreatedBy(models.Ticket.created_by_id, 'Created By',
                        options=[('1', 'User With ID 1'), ('2', 'User with ID 2, etc..')])
    ]


class StatusView(UserRequiredMixin, ModelView):
    pass


class TicketStatusView(UserRequiredMixin, ModelView):
    form_columns = ('ticket', 'status', 'description', 'created_by',)


admin.add_view(TicketView(models.Ticket, db.session))
admin.add_view(StatusView(models.Status, db.session))
admin.add_view(TicketStatusView(models.TicketStatus, db.session))
