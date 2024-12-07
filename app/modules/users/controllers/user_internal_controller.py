import io

from app.config import bcrypt
from app.modules.common import exceptions, utils
from app.modules.users.services.user_internal_service import UserInternalService

class UserInternalController:

    def __init__(self, user_service: UserInternalService):
        self.user_service = user_service

    def create_user(self, data):
        try:
            password = data.get("password")
            password_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
            

            if not data:
                raise exceptions.UseCaseException(message="data missing")
            
            # Crear datos del usuario
            user_data = {
                "name": data.get("name"),
                "last_name": data.get("last_name"),
                "document_number": data.get("document_number"),
                "email": data.get("email"),
                "password": password_hash,
                "gender": data.get("gender"),
                "user_type": data.get("user_type"),
                "dependency": data.get("dependency"),
            }


            # Llamar al servicio para crear el usuario
            result = self.user_service.create_user_internal(user_data)

            return utils.Response(result, status=utils.Status.CREATED_201)

        except exceptions.UseCaseException as e:
            return utils.Response({"message": str(e)}, status=400)

        except Exception as e:
            return utils.Response({"error": f"Unexpected error: {str(e)}"},
                                  status=utils.Status.INTERNAL_SERVER_ERROR_500)
