from app.config import db
from datetime import datetime, timezone


class IngressRecord(db.Model):
    __tablename__ = 'ingress_records'

    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    suggestions_comments = db.Column(db.String(50), nullable=True)
    protection_notice = db.Column(db.String(20), nullable=True)
    services_library = db.Column(db.String(20), nullable=True)
    reason = db.Column(db.String(20), default="other", nullable=True)
    site = db.Column(db.String(50), default="Biblioteca sede 4 vientos")
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='ingress_records')

    def __repr__(self):
        return f'<IngressRecord {self.id}>'
