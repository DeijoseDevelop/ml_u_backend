import io
import flask
import logging

from app.modules.create_user import controllers, services
from app.modules.user_recognition import entities
from app.modules.common import interfaces, utils, decorators, validations


class UserExternalCreateView(interfaces.APIView):

    def post(self):
        try:
            # Obtener datos de la solicitud
            user_data = flask.request.form
            picture = flask.request.files.get("picture")
            io_picture = io.BytesIO(picture.stream.read())
            
            validations.validate_user_data_with_picture(user_data=user_data, picture=picture)   
            image_manager = entities.ImageManager()
            face_detector = entities.FaceDetector()
            user_service = services.UserExternalService(image_manager, face_detector)
            user_controller = controllers.UserExternalController(user_service)

            # Llamar al controlador para crear el usuario
            return user_controller.create_user(user_data, io_picture)
        
        except Exception as e:
            logging.error(f"Error processing request: {e}")
            return utils.Response({"message": str(e)}, status=500)