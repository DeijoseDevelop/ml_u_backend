import logging
from app.config import db
from sqlalchemy.exc import SQLAlchemyError
from app.modules.user_recognition.models import User


class UserRepository:

    @staticmethod
    def create_user(data: dict) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    @staticmethod
    def get_user_by_document_number(document_number: str) -> User:
        try:
            user = User.query.filter_by(document_number=document_number).first()
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por documento: {e}")
            return None
    
    @staticmethod
    def get_user_by_email(email: str) -> User:
        try:
            user = User.query.filter_by(email=email).first()
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por correo electrónico: {e}")
            return None
