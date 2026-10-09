"""Visitor messages submitted through the contact form."""

from datetime import datetime, timezone

from . import db


class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(254), nullable=False)
    purpose = db.Column(db.String(40), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime(timezone=False),
        nullable=False,
        # MySQL DATETIME has no timezone storage; persist naive UTC values.
        default=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
    )
