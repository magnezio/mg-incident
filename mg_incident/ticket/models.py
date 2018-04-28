import datetime

from sqlalchemy import Column, ForeignKey, \
        Integer, String, Boolean, DateTime

from sqlalchemy.orm import relationship

from mg_incident import db
from mg_incident.account.models import approlestatus_ticketstatus


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    ticket_statuses_tracking = relationship('TicketStatusTracking', backref='ticket_status')
    user_roles = relationship('AppRoleStatus',
                              uselist=True,
                              secondary=approlestatus_ticketstatus,
                              )
    predefined = Column(Boolean, default=False)

    def __repr__(self):
        return self.name


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                           nullable=False)
    assigned_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'))
    assigned_to_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'))
    ticket_statuses_tracking = relationship('TicketStatusTracking', backref='ticket')
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)

    # self-referential
    parent_id = Column(Integer, ForeignKey('ticket.id'))
    children = relationship('Ticket', backref=backref('parent', remote_side=[id]))

    def __repr__(self):
        description = ' '
        if self.description:
            description = ' (' + str(self.description) + ') '
        return '<id: {}> {} {} <created by: >'.format(self.id, self.name, description, self.created_by.username)


class TicketStatusTracking(db.Model):
    __tablename__ = 'ticket_status_tracking'
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)
    ticket_id = Column(Integer, ForeignKey('ticket.id', on_delete='CASCADE'),
                       nullable=False)
    ticket_status_id = Column(Integer, ForeignKey('ticket_status.id', on_delete='SET NULL'),
                              nullable=False)
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                           nullable=False)
