from sqlalchemy import Column, PrimaryKeyConstraint, ForeignKey, \
    Integer, String, Boolean, DateTime
from sqlalchemy.orm import relationship, backref
from flask_security import (
    UserMixin, RoleMixin
)
from mg_incident import db


appuser_approle = db.Table(
    'appuser_approle',
    Column(
        'appuser_id', Integer, ForeignKey('appuser.id', ondelete='SET NULL')
    ),
    Column(
        'approle_id', Integer, ForeignKey('approle.id', ondelete='SET NULL')
    ),
    PrimaryKeyConstraint('appuser_id', 'approle_id')
)


class AppRole(db.Model, RoleMixin):
    __tablename__ = 'approle'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    description = Column(String(255), unique=True, nullable=False)
    users = relationship(
        'AppUser',
        uselist=True,
        backref=backref('roles', lazy='dynamic'),
        lazy='dynamic',
        secondary=appuser_approle
    )
    is_predefined = Column(Boolean, default=False)

    def __repr__(self):
        return self.name


class AppUser(db.Model, UserMixin):
    __tablename__ = 'appuser'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)
    active = Column(Boolean)
    password = Column(String(255))
    last_login_at = Column(DateTime())
    current_login_at = Column(DateTime())
    last_login_ip = Column(String(100))
    current_login_ip = Column(String(100))
    login_count = Column(Integer)
    confirmed_at = Column(DateTime())

    def __repr__(self):
        return "{} <{}>".format(self.username, self.email)
