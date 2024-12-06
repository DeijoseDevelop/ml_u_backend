import io

# from app.config import bcrypt
from app.modules.common import exceptions, utils
from app.modules.create_user.services.user_external_service import UserExternalService

class UserExternalController:

    def __init__(self, user_service: UserExternalService):
        self.user_service = user_service

    def create_user(self, data, image_bytes: io.BytesIO):
        try:
            # password = data.get("password")
            # password_hash = bcrypt.generate_password_hash(password=password).decode('utf-8')
            # "password": password_hash,

            if not data or not image_bytes:
                raise exceptions.UseCaseException(message="Picture or data missing")
            
            # Crear datos del usuario
            user_data = {
                "name": data.get("name"),
                "last_name": data.get("last_name"),
                "document_number": data.get("document_number"),
                "email": data.get("email"),
                "gender": data.get("gender"),
                "user_type": data.get("user_type"),
                "dependency": data.get("dependency"),
                "academic_program": data.get("academic_program")
            }


            # Llamar al servicio para crear el usuario
            result = self.user_service.create_user_with_face(user_data, image_bytes)

            return utils.Response(result, status=utils.Status.CREATED_201)

        except exceptions.UseCaseException as e:
            return utils.Response({"message": str(e)}, status=400)

        except Exception as e:
            return utils.Response({"error": f"Unexpected error: {str(e)}"},
                                  status=utils.Status.INTERNAL_SERVER_ERROR_500)
