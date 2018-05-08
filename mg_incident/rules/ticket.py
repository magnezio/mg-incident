from sqlalchemy.sql import func
from wtforms import ValidationError

from mg_incident import db
from mg_incident.models import AppRole, AppUser, Ticket, TicketStatus, TicketStatusTracking


def check_ticket_status_for_user(ticket_status_name, user):
    available_statuses = db.session.query(TicketStatus.name).join(
        TicketStatus.approles
    ).filter(
        AppRole.id.in_(r.id for r in user.roles)
    ).all()

    if not ticket_status_name in [s.name for s in available_statuses]:
        raise ValidationError('The selected ticket status is not available for your role')


def update_latest_status(ticket_status, ticket):
    ticket.latest_status = ticket_status


# status_chain = [
#     'New',
#     'In Progress',
#     [
#         'Pending Customer',
#         'Pending Vendor',
#         'Pending Maintenance',
#         'Transferred',
#     ],
#     'Solved',
#     'Closed',
# ]

# class StatusNames():
#     new = 'New'
#     in_progress = 'In Progress'
#     pending_customer = 'Pending Customer'
#     pending_vendor = 'Pending Vendor'
#     pending_maintenance = 'Pending Maintenance'
#     transferred = 'Transferred'
#     solved = 'Solved'
#     closed = 'Closed'


def get_latest_status(ticket):
    t = db.session.query(
        TicketStatusTracking.ticket_status,
        TicketStatusTracking.created_by,
        func.max(TicketStatusTracking.created_at)
    ).group_by(
        TicketStatusTracking.ticket_status,
        TicketStatusTracking.created_by
    ).filter(
        TicketStatusTracking.ticket==ticket
    ).first()
    return t.ticket_status, t.created_by
