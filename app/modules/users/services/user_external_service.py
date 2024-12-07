import io
import logging
from app.modules.user_recognition import entities
from app.modules.users import repositories
from app.modules.common import exceptions



class UserExternalService:

    def __init__(self, image_manager: entities.ImageManager, face_detector: entities.FaceDetector):
        self.image_manager = image_manager
        self.face_detector = face_detector
        self.repository = repositories.UserRepository()

    def create_user_with_face(self, user_data: dict, image_bytes: io.BytesIO) -> dict:
        
        try:
        # Procesar la imagen
            frame = entities.Frame()
            frame.set_value(self.image_manager.convert_bytes_to_cv2_image(image_bytes))
            rgb_image = frame.convert_to_rgb().get_rgb_value()
            face_encodings = self.face_detector.get_face_encodings(rgb_image)

            if not face_encodings:
             raise exceptions.UseCaseException(message="No se detectó ninguna cara en la imagen.")

        # Solo usamos la primera cara encontrada
            face_encoding = face_encodings[0]
            user_data['face_encoding'] = face_encoding.tolist()
        
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
       