

from app.config import bcrypt
from app.modules.common import exceptions, utils
from app.modules.users.services.user_service import UserService


class UserController:
    
    def __init__(self, user_service: UserService):
        self.user_service = user_service
        
        
    def update_user_external(self, user_id: int, data):
        try:
            password = data.get("password")
            if password:
                password_hash = bcrypt.generate_password_hash(password=password).decode('utf-8') 
            else:
                user = self.user_service.get_user_by_id(user_id=user_id)
                password_hash = user.password
            
            user_data = {
                "name": data.get("name"),
                "last_name": data.get("last_name"),
                "document_number": data.get("document_number"),
                "email": data.get("email"),
                "password": password_hash,
                "gender": data.get("gender"),
                "user_type": data.get("user_type"),
                "dependency": data.get("dependency"),
                "academic_program": data.get("academic_program"),
            }
            
            user_data = {key: value for key, value in user_data.items() if value is not None}

            result = self.user_service.update_user_external(user_id=user_id, user_data=user_data)
            
            if result is None:
                return utils.Response({"message": "Error al actualizar el usuario"})
            
            return utils.Response(result, status=200)
        
        except exceptions.UseCaseException as e:
            return utils.Response({"message": str(e)}, status=400)

        except Exception as e:
            return utils.Response({"error": f"Unexpected error: {str(e)}"},
                                  status=utils.Status.INTERNAL_SERVER_ERROR_500)
            
            