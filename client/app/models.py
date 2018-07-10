# -*- coding: utf-8 -*-

from . import db


class User(db.Model):
    """User table."""

    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.Text, unique=True, index=True)

    def __repr__(self):
        return '<User %r>' % self.email
