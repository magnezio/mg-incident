from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship, backref

from flask_security import (
    UserMixin, RoleMixin
)

from mg_incident import db


class AppUser(db.Model, UserMixin):
    __tablename__ = 'appuser'
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), unique=True, nullable=False)
    email = Column(String(50), unique=True, nullable=False)


class AppRole(db.Model, RoleMixin):
    __tablename__ = 'approle'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), unique=True, nullable=False)
    descr = Column(String(255))