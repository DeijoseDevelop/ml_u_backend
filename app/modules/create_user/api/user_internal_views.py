import flask
import logging

from app.modules.create_user import controllers, services
from app.modules.common import interfaces, utils, decorators, validations


class UserInternalCreateView(interfaces.APIView):

    def post(self):
        try:
            # Obtener datos de la solicitud
            user_data = flask.request.form
            validations.validate_user_data(user_data=user_data) 
            user_service = services.UserInternalService()
            user_controller = controllers.UserInternalController(user_service)

            # Llamar al controlador para crear el usuario
            return user_controller.create_user(user_data)
        
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)