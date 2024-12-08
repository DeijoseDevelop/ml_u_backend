import io
import flask
import logging
from flask_jwt_extended import jwt_required

from app.modules.users import controllers, services
from app.modules.user_recognition import entities
from app.modules.common import interfaces, utils, validations


class UserExternalCreateView(interfaces.APIView):
    
    # @jwt_required()
    def post(self):
        try:
            print(flask.request.headers)
            # Obtener datos de la solicitud
            user_data = flask.request.form
            print(user_data)
            picture = flask.request.files.get("picture")
            print(picture)
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