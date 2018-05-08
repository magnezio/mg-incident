from sqlalchemy import (
    Column, PrimaryKeyConstraint, ForeignKey, Integer, String, Boolean, DateTime
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
    latest_status_id = Column(Integer, ForeignKey('ticket_status.id', ondelete='SET NULL'))
    created_by = relationship(
        AppUser,
        backref=backref('tickets_created_by', uselist=True, lazy='dynamic'),
        foreign_keys=[created_by_id, ],
        lazy='joined'
    )
    assigned_by = relationship(
        AppUser, backref=backref('tickets_assigned_by', uselist=True, lazy='dynamic'),
        foreign_keys=[assigned_by_id, ],
        lazy='joined'
    )
    assigned_to = relationship(
        AppUser, backref=backref('tickets_assigned_to', uselist=True, lazy='dynamic'),
        foreign_keys=[assigned_to_id, ],
        lazy='joined'
    )
    from_ticket = relationship(
        'Ticket',
        backref=backref('chained_tickets', remote_side=[id, ], uselist=True, lazy='subquery'),
        lazy='joined'
    )
    latest_status = relationship(
        'TicketStatus', backref=backref('curent_tickets', uselist=True, lazy='dynamic'),
        lazy='joined'
    )

    def __repr__(self):
        return "#{} {}".format(self.id, self.name)


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    is_predefined = Column(Boolean, default=False)
    approles = relationship(
        'AppRole',
        backref=backref('ticket_statuses', uselist=True, lazy='dynamic'),
        lazy='joined',
        secondary='ticket_status_approle',
        uselist=True
    )

    def __repr__(self):
        return self.name


ticket_status_approle = db.Table(
    'ticket_status_approle',
    Column(
        'ticket_status_id',
        Integer,
        ForeignKey('ticket_status.id', ondelete='SET NULL'),
        nullable=False
    ),
    Column(
        'approle_id',
        Integer,
        ForeignKey('approle.id', ondelete='SET NULL'),
        nullable=False
    ),
    PrimaryKeyConstraint('ticket_status_id', 'approle_id')
)


class TicketStatusTracking(db.Model):
    __tablename__ = 'ticket_status_tracking'
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, onupdate=func.now())
    ticket_id = Column(Integer, ForeignKey('ticket.id', ondelete='CASCADE'),
                       nullable=False)
    ticket_status_id = Column(Integer, ForeignKey('ticket_status.id', ondelete='SET NULL'),
                              nullable=False)
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                           nullable=False)
    ticket = relationship(
        Ticket,
        backref=backref('ticket_status_trackings', uselist=True, lazy='dynamic'),
        lazy='joined'
    )
    ticket_status = relationship(
        TicketStatus,
        backref=backref('ticket_status_trackings', uselist=True, lazy='dynamic'),
        lazy='joined'
    )
    created_by = relationship(
        AppUser,
        backref=backref('ticket_status_trackings', uselist=True, lazy='dynamic'),
        lazy='joined'
    )
