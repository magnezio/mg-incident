import datetime

from sqlalchemy import Column, ForeignKey, \
        Integer, String, Boolean, DateTime

from sqlalchemy.orm import relationship

from mg_incident import db


class Status(db.Model):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    ticket_statuses = relationship('TicketStatus', backref='status')
    predefined = Column(Boolean, default=False)


class Ticket(db.Model):
    __tablename__ = 'ticket'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    description = Column(String(255))
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                            nullable=False)
    assigned_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'))
    assigned_to_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'))
    ticket_statuses = relationship('TicketStatus', backref='ticket')
    created_at = Column(DateTime, default=datetime.datetime.now, nullable=False)


class TicketStatus(db.Model):
    __tablename__ = 'ticket_status'
    id = Column(Integer, primary_key=True)
    description = Column(String(255))
    ticket_id = Column(Integer, ForeignKey('ticket.id', on_delete='CASCADE'),
                       nullable=False)
    status_id = Column(Integer, ForeignKey('status.id', on_delete='SET NULL'),
                       nullable=False)
    created_by_id = Column(Integer, ForeignKey('appuser.id', ondelete='SET NULL'),
                           nullable=False)
