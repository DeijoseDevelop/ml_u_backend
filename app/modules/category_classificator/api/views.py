import logging

import flask
from marshmallow import ValidationError

from app.modules.common import interfaces, utils, decorators
from app.modules.category_classificator import services, repositories, controllers
from app.modules.category_classificator.api import schemas


class PredictCategoryClassificatorView(interfaces.APIView):
    decorators = [decorators.x_api_key_required]

    def __init__(self, predict_service=None):
        if predict_service is None:
            predict_repository = repositories.PredictRepository(
                model_path=flask.current_app.config.get("model", None),
                vectorizer_path=flask.current_app.config.get("vectorizer", None),
            )
            self.predict_service = services.PredictService(repository=predict_repository)
        else:
            self.predict_service = predict_service

    def post(self):
        try:
            logging.info("Encabezados de la petición: %s", flask.request.headers)
            request_data = flask.request.get_json(force=True)
            if request_data is None:
                return utils.Response(
                    response={"message": "El tipo de contenido debe ser 'application/json'."},
                    status=utils.Status.BAD_REQUEST_400
                )

            schema = schemas.PredictRequestSchema()
            data = schema.load(request_data)

            prediction = self.predict_service.call(text=request_data['text'])

            return utils.Response(response={"data": prediction}, status=utils.Status.OK_200)

        except ValidationError as err:
            return utils.Response(response={"errors": err.messages}, status=utils.Status.BAD_REQUEST_400)
        except Exception as error:
            logging.error(f"Error en PredictCategoryClassificatorView.post: {error}")
            return utils.Response(
                response={"message": "Ocurrió un error interno."},
                status=utils.Status.INTERNAL_SERVER_ERROR_500
            )


class TrainModelCategoryClassificatorView(interfaces.APIView):
    def __init__(self, train_model_service=None, clean_data_service=None):
        if train_model_service is None or clean_data_service is None:
            clean_data_repository = repositories.CleanDataRepository(
                file_path=flask.current_app.config.get("classification_data", None),
            )
            clean_data_service = services.CleanDataService(repository=clean_data_repository)

            train_model_repository = repositories.TrainModelRepository(
                model_path=flask.current_app.config.get("model", None),
                vectorizer_path=flask.current_app.config.get("vectorizer", None),
            )
            train_model_service = services.TrainModelService(repository=train_model_repository)

        self.train_model_service = train_model_service
        self.clean_data_service = clean_data_service

    def post(self):
        try:
            texts, labels = self.clean_data_service.call()

            self.train_model_service.call(texts=texts, labels=labels)

            return utils.Response(
                response={"message": "Entrenamiento completado con éxito."},
                status=utils.Status.OK_200
            )

        except Exception as error:
            logging.error(f"Error en TrainModelCategoryClassificatorView.post: {error}")
            return utils.Response(
                response={"message": "Ocurrió un error interno durante el entrenamiento."},
                status=utils.Status.INTERNAL_SERVER_ERROR_500
            )
