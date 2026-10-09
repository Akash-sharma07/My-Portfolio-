"""Admin accounts used only for authenticating the private message inbox."""

from werkzeug.security import check_password_hash

from . import db


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def check_password(self, candidate: str) -> bool:
        return check_password_hash(self.password_hash, candidate)
