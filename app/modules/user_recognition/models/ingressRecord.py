from app.config import db
from datetime import datetime, timezone


class IngressRecord(db.Model):
    __tablename__ = 'ingress_records'

    id = db.Column(db.Integer, primary_key=True)
    time_stamp = db.Column(db.DateTime, default=datetime.now(timezone.utc), nullable=False)
    suggestions_comments = db.Column(db.String(50), unique=True, nullable=False)
    proteccion_notice = db.Column(db.String(20), nullable=False)
    services_library = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='ingress_records')

    def __repr__(self):
        return f'<IngressRecord {self.id}>'
