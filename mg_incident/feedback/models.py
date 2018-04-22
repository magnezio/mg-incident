from sqlalchemy import Column, ForeignKey, Integer, String

from mg_incident.auth import UserRequiredMixin
from mg_incident import db


class Feedback(db.Model):
    __tablename__ = 'feedback'
    id = Column(Integer, primary_key=True)
