from sqlalchemy.sql import func

from mg_incident.models import AppRole, AppUser, Ticket, TicketStatus, TicketStatusTracking


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


def check_new_status(ticket_status):
    pass
