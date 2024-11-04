import flask

from app.modules.category_classificator.api import views


category_classificator_app = flask.Blueprint('category_classificator', __name__)

category_classificator_app.add_url_rule(
    '/api/v1/classificator/predict/',
    view_func=views.PredictCategoryClassificatorView.as_view("predict_category_classificator_view"), methods=['POST'],
)

category_classificator_app.add_url_rule(
    '/api/v1/classificator/train/',
    view_func=views.TrainModelCategoryClassificatorView.as_view("train_category_classificator_view"), methods=['POST'],
)