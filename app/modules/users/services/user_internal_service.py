import io
import logging
from app.modules.user_recognition import entities
from app.modules.users import repositories
from app.modules.common import exceptions



class UserInternalService:

    def __init__(self):
        self.repository = repositories.UserRepository()

    def create_user_internal(self, user_data: dict) -> dict:
        
        try:
            user = self.repository.get_user_by_document_number(user_data.get("document_number"))
            if user:
                logging.warning(f"Intento de crear usuario duplicado con document_number: {user_data.get('document_number')}")
                raise exceptions.UseCaseException(message="El número de documento ya está en uso.")
            
            user_email = self.repository.get_user_by_email(user_data.get("email"))
            if user_email:
                logging.warning(f"Intento de crear usuario duplicado con email: {user_data.get('email')}")
                raise exceptions.UseCaseException(message="Email ya esta en uso")
        
        # Guardar el usuario en la base de datos
            user = self.repository.create_user(user_data)
            return {"message": "Usuario creado exitosamente", "user_id": user.id}
            
        except Exception as e:
            raise exceptions.UseCaseException(message=str(e))
       