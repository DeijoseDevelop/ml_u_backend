import flask

from app.modules.user_recognition.api import views


user_recognition_app = flask.Blueprint('user_recognition', __name__)

user_recognition_app.add_url_rule(
    '/api/v1/recognition/detect/',
    view_func=views.UserRecognitionView.as_view("user_recognition_view"), methods=['POST'],
)
