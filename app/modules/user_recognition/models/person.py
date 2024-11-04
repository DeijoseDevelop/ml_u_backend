from app.config import db


class Person(db.Model):
    __tablename__ = 'persons'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    document_number = db.Column(db.String(50), unique=True, nullable=False)
    gender = db.Column(db.String(20), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)
    dependency = db.Column(db.String(50), nullable=False)
    academic_program = db.Column(db.String(100), nullable=True)
    face_encoding = db.Column(db.PickleType, nullable=False)  # Asegúrate de que este campo está definido


    def __repr__(self):
        return f'<Person {self.name}>'
