from app.config import db


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=True)
    gender = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    dependency = db.Column(db.String(50), nullable=True)
    academic_program = db.Column(db.String(100), nullable=True)
    face_encoding = db.Column(db.PickleType, nullable=True)  # Asegúrate de que este campo está definido
    ingress_records = db.relationship('IngressRecord', back_populates='user', cascade='all, delete-orphan')
    def __repr__(self):
        return f'<User {self.name}>'
