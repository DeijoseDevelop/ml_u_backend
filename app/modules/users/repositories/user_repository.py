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
            logging.error(f"Error al traer usuarios: {e}")
            return None

    def get_all_users_by_is_internal(self, is_internal=False):
        try:
            users = User.query.filter_by(is_internal=is_internal)
            return users
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar los usuarios: {e}")
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
        
    def get_user_by_id(self, user_id: int) -> User:

        try:
            user = User.query.filter_by(id=user_id).first()
            print(user)
            return user
        except SQLAlchemyError as e:
            logging.error(f"Error al consultar el usuario por id: {e}")
            return None
    
    def delete_user(self, user: User) -> bool:
        try:
            db.session.delete(user)
            db.session.commit()
            return True
        except SQLAlchemyError as e:
            db.session.rollback() 
            logging.error(f"Error al Eliminar usuario: {e}")
            return False
        
    
    def update_user(self, user_id: int, data_user) -> User:
        try:
            print("type os user_data: ", type(data_user))
            print("contect user_data: ", data_user)
            user = User.query.filter_by(id=user_id).first()
            print("user: ", user)
            if not isinstance(data_user, dict):
                raise ValueError(f"Se esperaba un diccionario para data_user, pero se recibió: {type(data_user)}")
        
            if user is None:
                logging.error(f"Usuario con ID {user_id} no encontrado.")
                return None
            
            for key, value in data_user.items():
                if value is not None and hasattr(user, key):
                    print("keys: ", key)
                    print("values: ", value)
                    setattr(user, key, value)
            db.session.commit()
            
            logging.info(f"Usuario con ID {user_id} actualizado exitosamente.")
            return user
        
        except SQLAlchemyError as e:
            db.session.rollback()  
            logging.error(f"Error al actualizar usuario con ID {user_id}: {e}")
            return None
        