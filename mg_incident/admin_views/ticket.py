from flask_security import current_user
from flask_admin.contrib.sqla import ModelView
from wtforms import ValidationError

from mg_incident import db, admin
from mg_incident.auth import AdminRequiredMixin, ManagerRequiredMixin, \
    WorkerRequiredMixin, UserRequiredMixin
from mg_incident.models import Ticket, TicketStatus, TicketStatusTracking, AppRole
from mg_incident.admin_views import formatters
from mg_incident.rules.ticket import check_ticket_status_for_user


class TicketView(WorkerRequiredMixin, UserRequiredMixin, ModelView):
    column_list = ['id', 'name', 'from_ticket', 'assigned_to',
                   'assigned_by', 'created_by', 'created_at', 'updated_at', ]
    column_filters = [
        'from_ticket.name',
        'from_ticket.id',
        'created_by.username',
        'assigned_by.username',
        'assigned_to.username',
    ]
    form_columns = ['name', 'description', 'assigned_to', 'from_ticket', ]
    inline_models = [TicketStatusTracking, ]
    column_type_formatters = formatters.DEFAULT_FORMATTERS
    can_view_details = True
    can_delete = True

    def on_model_delete(self, model):
        if model.chained_tickets:
            raise ValidationError("You can't deleting tickets that have child records")
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_by = current_user
        if not model.assigned_to == form.assigned_to:
            model.assigned_by = current_user


class TicketStatusView(AdminRequiredMixin, ModelView):
    column_list = ['name', 'description', 'approles', ]
    column_searchable_list = ['name', 'description', ]
    column_filters = ['approles.name', ]
    form_columns = ['name', 'description', 'approles', ]
    can_view_details = True
    can_delete = True

    def on_model_delete(self, model):
        if model.is_predefined:
            raise ValidationError('Predefined status can not be deleted.')

    def on_model_change(self, form, model, is_created):
        if model.is_predefined and not is_created:
            raise ValidationError('Predefined status can not be changed.')


class TicketStatusTrackingView(WorkerRequiredMixin, UserRequiredMixin, ModelView):
    form_columns = ['ticket', 'ticket_status', 'description', ]
    column_filters = [
        'ticket.name', 'ticket.id', 'ticket_status.name', 'created_by.username',
    ]
    column_searchable_list = ['description', ]
    column_type_formatters = formatters.DEFAULT_FORMATTERS
    
    def on_model_change(self, form, model, is_created):
        if is_created:
            model.created_by = current_user

        check_ticket_status_for_user(form.ticket_status.data.name, current_user)


admin.add_views(
    TicketView(Ticket, db.session),
    TicketStatusView(TicketStatus, db.session),
    TicketStatusTrackingView(TicketStatusTracking, db.session)
)
