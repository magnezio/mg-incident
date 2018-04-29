from sqlalchemy import (
    Column, ForeignKey, Integer, String, Boolean, DateTime
)
from sqlalchemy.sql import func
from sqlalchemy.orm import backref, relationship

from mg_incident import db
from mg_incident.models import AppUser


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                           nullable=False)
    assigned_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                            nullable=False)
    assigned_to_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                            nullable=False)
    from_ticket_id = Column(Integer, ForeignKey('ticket.id', ondelete='SET NULL'))
    created_by = relationship(
        AppUser,
        backref=backref('tickets_created_by', lazy='dynamic'),
        foreign_keys=[created_by_id, ],
        lazy='joined'
    )
    assigned_by = relationship(
        AppUser, backref=backref('tickets_assigned_by', lazy='dynamic'),
        foreign_keys=[assigned_by_id, ],
        lazy='joined'
    )
    assigned_to = relationship(
        AppUser, backref=backref('tickets_assigned_to', lazy='dynamic'),
        foreign_keys=[assigned_to_id, ],
        lazy='joined'
    )
    from_ticket = relationship(
        'Ticket',
        backref=backref('chained_tickets', remote_side=[id, ], uselist=True, lazy='dynamic'),
        lazy='dynamic'
    )
    # ticket_statuses_tracking = relationship('TicketStatusTracking', backref='ticket')
    # children = relationship('Ticket', backref=backref('parent', remote_side=[id]))

    def __repr__(self):
        return self.name


# class TicketStatus(db.Model):
#     __tablename__ = 'ticket_status'
#     id = Column(Integer, primary_key=True)
#     name = Column(String(255), unique=True, nullable=False)
#     description = Column(String(255))
#     ticket_statuses_tracking = relationship('TicketStatusTracking', backref='ticket_status')
#     # user_roles = relationship('AppRoleStatus',
#     #                           uselist=True,
#     #                           secondary=approlestatus_ticketstatus,
#     #                           )
#     predefined = Column(Boolean, default=False)

#     def __repr__(self):
#         return self.name


# class TicketStatusTracking(db.Model):
#     __tablename__ = 'ticket_status_tracking'
#     id = Column(Integer, primary_key=True)
#     description = Column(String(255))
#     # created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
#     ticket_id = Column(Integer, ForeignKey('ticket.id', on_delete='CASCADE'),
#                        nullable=False)
#     ticket_status_id = Column(Integer, ForeignKey('ticket_status.id', on_delete='SET NULL'),
#                               nullable=False)
#     created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
#                            nullable=False)
