from flask_admin.contrib.sqla import ModelView
from flask_security import current_user
from sqlalchemy.sql.functions import current_user
from wtforms import ValidationError

from mg_incident import db, admin
from mg_incident.auth import UserRequiredMixin
from mg_incident.models import Ticket
from mg_incident.admin_views import formatters


class TicketView(ModelView):
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
    column_type_formatters = formatters.DEFAULT_FORMATTERS
    can_view_details = True
    can_delete = True

    def on_model_delete(self, model):
        if model.chained_tickets:
            raise ValidationError("You can't deleting tickets that have child records")
    
    def on_model_change(self, form, model, is_created):
        from flask_security import current_user
        if is_created:
            model.created_by = current_user
        if not model.assigned_to == form.assigned_to:
            model.assigned_by = current_user

            
# class TicketStatusView(UserRequiredMixin, ModelView):
#     column_list = ('name', 'description', 'user_roles')
#     column_searchable_list = ('name', 'user_roles.name')
#     column_filters = ('name', 'user_roles.name')
# =======
# 
# class TicketStatusView(UserRequiredMixin, ModelView):
#     column_list = ('name', 'description', 'user_roles')
#     pass
# =======
#     def delete_model(self, model):
#         """
#             Delete model.
#             :param model:
#                 Model to delete
#         """
#         try:
#             self.on_model_delete(model)
#             if not model.children:
#                 self.session.flush()
#                 self.session.delete(model)
#                 self.session.commit()
#             if model.children:
#                 return False
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

#             self.session.rollback()

#             return False
#         else:
#             self.after_model_delete(model)

#         return True
#

# =======

# class TicketStatusTrackingView(UserRequiredMixin, ModelView):
#     form_columns = ('ticket', 'ticket_status', 'description', 'created_by', 'created_at',)
#     column_filters = ('ticket.name', 'ticket_status.name', 'description', 'created_by.username',)
#     column_searchable_list = ('ticket.id', 'ticket_status.name', 'description',)
#     form_columns = ('ticket', 'ticket_status', 'description', 'created_by', 'created_at')
    
# # =======

# class StatusView(UserRequiredMixin, ModelView):
#     form_excluded_columns = ('predefined',)

#     def on_model_delete(self, model):
#         if model.predefined:
#             raise ValidationError('Predefined status can not be deleted.')

#     def on_model_change(self, form, model, is_created):
#         if model.predefined:
#             raise ValidationError('Predefined status can not be changed.')

#     def delete_model(self, model):
#         """
#             Delete model.

#             :param model:
#                 Model to delete
#         """
#         try:
#             self.on_model_delete(model)
#             if not model.predefined:
#                 self.session.flush()
#                 self.session.delete(model)
#                 self.session.commit()
#             if model.predefined:
#                 return False
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(gettext('Failed to delete record. %(error)s', error=str(ex)), 'error')

#             self.session.rollback()

#             return False
#         else:
#             self.after_model_delete(model)

#         return True


# class TicketStatusView(UserRequiredMixin, ModelView):
#     form_columns = ('ticket', 'status', 'description',)

#     def create_model(self, form):
#         try:
#             model = self.model()
#             model.created_by_id = current_user.id
#             form.populate_obj(model)
#             self.session.add(model)
#             self._on_model_change(form, model, True)
#             self.session.commit()
#         except Exception as ex:
#             if not self.handle_view_exception(ex):
#                 flash(gettext('Failed to create record. %(error)s', error=str(ex)), 'error')

#             self.session.rollback()

#             return False
#         else:
#             self.after_model_change(form, model, True)

#         return model


admin.add_views(
    TicketView(Ticket, db.session)
)
