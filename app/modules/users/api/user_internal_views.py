import flask
import logging
from flask_jwt_extended import jwt_required

from app.modules.users import controllers, services
from app.modules.common import interfaces, utils, validations


class UserInternalCreateView(interfaces.APIView):

    # @jwt_required()
    def post(self):
        try:
            # Obtener datos de la solicitud
            user_data = flask.request.form if flask.request.form else flask.request.json
            logging.debug(f"Received user data: {user_data}")

            validations.validate_user_data(user_data=user_data)
            user_service = services.UserInternalService()
            user_controller = controllers.UserInternalController(user_service)

            # Llamar al controlador para crear el usuario
            return user_controller.create_user(user_data)
        
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)