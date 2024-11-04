import io
import base64
import logging

import flask

from app.modules.common import interfaces, utils, decorators
from app.modules.user_recognition import services, repositories, entities
from app.modules.user_recognition import controllers



class UserRecognitionView(interfaces.APIView):

    @decorators.x_api_key_required
    def post(self):
        try:
            image_manager = entities.ImageManager()
            face_detector = entities.FaceDetector()
            controller = controllers.RecognitionController(
                image_manager=image_manager,
                recognition_service=services.RecognitionService(
                    repository=repositories.RecognitionRepository(
                        image_manager=image_manager,
                        face_detector=face_detector
                    )
                )
            )

            if "picture" not in flask.request.files:
                return utils.Response({"message": 'Picture not found'}, status=utils.Status.NOT_FOUND_404)

            picture = flask.request.files["picture"]
            io_picture = io.BytesIO(picture.stream.read())

            recognition = controller.detect_face(io_picture)

            if recognition is None:
                return utils.Response({"message": 'Recognition failed'}, status=utils.Status.BAD_REQUEST_400)

            recognition["image"].seek(0)
            recognition["image"] = base64.b64encode(recognition["image"].getvalue()).decode("ascii")

            return utils.Response(recognition)

            # return flask.send_file(
            #     recognition["image"],
            #     mimetype='image/jpeg',
            #     as_attachment=True,
            #     download_name='image.jpg'
            # )
        except Exception as e:
            logging.error(f"Error in UserRecognitionView POST: {e}")

            return utils.Response({"message": str(e)}, status=utils.Status.BAD_REQUEST_400)
