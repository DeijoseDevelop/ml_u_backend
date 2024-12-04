
from flask_jwt_extended import create_access_token
from app.modules.common import exceptions, utils
from .service import UserInternalAuth

class UserInternalAuthController:
    
    def __init__(self, user_auth_service: UserInternalAuth):
        self.user_auth_service = user_auth_service
        
    
    def auth_with_jwt(self, data):
        try:
            
            if not data:
                return utils.Response({"error": "Datos requeridos"}, status=400 )
            
            email = data.get("email")
            password = data.get("password")
            
            user = self.user_auth_service.auth_user_internal(email, password)
            if not user:
                return utils.Response({"error": "Usuario no encontrado"}, status=404)
            
            acces_token = create_access_token(identity=email)
            
            return utils.Response({"access_token": acces_token}, status=200)
            
        except exceptions.UseCaseException as e:
            return utils.Response({"message": str(e)}, status=400)
        
        except Exception as e:
            return utils.Response({"error": f"Unexpected error: {str(e)}"}, status=500)
            
            