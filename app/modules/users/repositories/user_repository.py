import logging
from app.config import db
from sqlalchemy.exc import SQLAlchemyError
from app.modules.user_recognition.models import User


class UserRepository:

    def create_user(self, data: dict) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def get_all_users(self):
        try:
            users = User.query.all()
            return users
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por documento: {e}")
            return None

    def get_all_users_by_is_internal(self, is_internal=False):
        try:
            users = User.query.filter_by(is_internal=is_internal)
            return users
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por documento: {e}")
            return None

    def get_user_by_document_number(self, document_number: str) -> User:
        try:
            user = User.query.filter_by(document_number=document_number).first()
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por documento: {e}")
            return None

    def get_user_by_email(self, email: str) -> User:
        try:
            user = User.query.filter_by(email=email).first()
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por correo electrónico: {e}")
            return None
