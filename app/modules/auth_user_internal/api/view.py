import flask
import logging

from app.modules.auth_user_internal import service, controller
from app.modules.common import interfaces, utils


class UserInternaAuthView(interfaces.APIView):
    
    def post(self):
        try:
            user_data = flask.request.form if flask.request.form else flask.request.json
            required_fields = ['email','password']
            
            if not all(field in user_data and user_data.get(field) for field in required_fields):
                return utils.Response({"message": "Ambos campos son requeridos"}, status=400)
            
            user_service = service.UserInternalAuth()
            user_controller = controller.UserInternalAuthController(user_auth_service=user_service)
            
            return user_controller.auth_with_jwt(user_data)
        
        except Exception as e:
            logging.error(f"Error proceesing request: {e}")
            return utils.Response({"message": str(e)}, status=500)
