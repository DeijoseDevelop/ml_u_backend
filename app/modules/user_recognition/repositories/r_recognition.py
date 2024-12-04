import io
import os
import pickle
import typing as t
import logging

import numpy as np
import cv2.typing
from scipy.spatial import KDTree
from flask import current_app

from app.modules.user_recognition import entities, models


class RecognitionRepository:

    def __init__(self, image_manager: entities.ImageManager, face_detector: entities.FaceDetector) -> None:
        self.face_detector = face_detector
        self.image_manager = image_manager

        cache_file = 'face_encodings_cache.pkl'

        with current_app.app_context():
            total_person_count = models.Person.query.count()
            self.data_manager = entities.DataManager(
                image_manager=image_manager,
                path=current_app.config.get("recognition_data"),
                face_detector=self.face_detector
            )

            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    cache_data = pickle.load(f)
                    cache_person_count = cache_data.get('person_count', 0)
                    if cache_person_count != total_person_count:
                        logging.info("El caché está desactualizado. Recargando datos desde la base de datos.")
                        self._load_data_from_database()
                        self._save_cache(cache_file, total_person_count)
                    else:
                        self.known_face_encodings = cache_data['encodings']
                        self.known_face_ids = cache_data['ids']
                        logging.info("Datos cargados desde el caché.")
            else:
                self._load_data_from_database()
                self._save_cache(cache_file, total_person_count)

        self.known_face_encodings = np.array(self.known_face_encodings)

        # Verificar que hay codificaciones faciales
        if self.known_face_encodings.size == 0:
            raise ValueError("No se encontraron codificaciones faciales. Asegúrate de que la base de datos contiene datos válidos.")

        # Asegurarse de que el array es bidimensional
        if self.known_face_encodings.ndim == 1:
            self.known_face_encodings = self.known_face_encodings.reshape(1, -1)

        logging.info(f"Shape of known_face_encodings: {self.known_face_encodings.shape}")

        # Ahora, inicializar el KDTree
        self.kd_tree = KDTree(self.known_face_encodings)

    def _load_data_from_database(self):
        users = models.User.query.all()
        self.known_face_encodings = []
        self.known_face_ids = []
        for user in users:
            encoding = user.face_encoding
            if encoding is not None and len(encoding) > 0:
                self.known_face_encodings.append(encoding)
                self.known_face_ids.append(user.id)
            else:
                logging.warning(f"Advertencia: La persona '{user.name}' no tiene una codificación facial válida.")
        logging.info(f"Número de codificaciones faciales cargadas: {len(self.known_face_encodings)}")

    def _save_cache(self, cache_file, person_count):
        # Guardar las codificaciones y los IDs en el archivo de caché
        cache_data = {
            'encodings': self.known_face_encodings,
            'ids': self.known_face_ids,
            'person_count': person_count
        }
        with open(cache_file, 'wb') as f:
            pickle.dump(cache_data, f)
        logging.info("Caché actualizado y guardado.")

    def detect_face(self, image_bytes: io.BytesIO) -> t.List[t.Dict[str, t.Any]]:
        cv2_image = self._convert_bytes_to_cv2_image(image_bytes)

        self._set_frame(cv2_image)
        rgb_image = self._convert_to_rgb_and_get_value(self.image_manager.get_frame())
        face_locations, face_encodings = self._detect_faces(rgb_image)
        return self._find_best_match(face_encodings, face_locations)

    def _convert_bytes_to_cv2_image(self, image_bytes: io.BytesIO) -> cv2.typing.MatLike:
        return self.image_manager.convert_bytes_to_cv2_image(data=image_bytes)

    def _set_frame(self, cv2_image: cv2.typing.MatLike) -> None:
        self.image_manager.set_frame(cv2_image)

    def _convert_to_rgb_and_get_value(self, frame: entities.Frame) -> cv2.typing.MatLike:
        rgb_image = frame.convert_to_rgb().get_rgb_value()
        return rgb_image

    def _detect_faces(self, rgb_image):
        face_locations = self.face_detector.get_face_locations(rgb_image)
        if not face_locations:
            return [], []

        face_encodings = self.face_detector.get_face_encodings(rgb_image, face_locations)
        return face_locations, face_encodings

    def _find_best_match(
        self,
        face_encodings: t.List[np.ndarray],
        face_locations: t.List[t.Tuple[int, int, int, int]]
    ) -> t.List[t.Dict[str, t.Any]]:

        data = []
        match_threshold = 0.6  # Ajusta el umbral según sea necesario

        if not face_encodings:
            # No se detectó ninguna cara
            return data

        # Procesar solo la primera cara
        face_encoding = face_encodings[0]
        (top, right, bottom, left) = face_locations[0]

        # Buscar la coincidencia más cercana en el KDTree
        distance, index = self.kd_tree.query(face_encoding)
        user_id = self.known_face_ids[index]

        if distance < match_threshold:
            # Obtener la información de la persona desde la base de datos
            with current_app.app_context():
                user = models.User.query.get(user_id)

            if user:
                name = user.name
                # Dibuja en la imagen
                self.image_manager.draw_rectangle(positions=(top, right, bottom, left), thickness=2)
                self.image_manager.draw_rectangle(positions=(bottom, right, bottom - 25, left), thickness=cv2.FILLED)
                self.image_manager.draw_text(name=name, positions=(top, right, bottom, left), thickness=2)

                # Preparar los datos para devolver
                detection = {
                    "name": user.name,
                    "document_number": user.document_number,
                    "gender": user.gender,
                    "user_type": user.user_type,
                    "dependency": user.dependency,
                    "academic_program": user.academic_program,
                    "matched": True,
                    "face_locations": {
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "left": left,
                    }
                }
            else:
                detection = {
                    "name": "Unknown",
                    "matched": False,
                    "face_locations": {
                        "top": top,
                        "right": right,
                        "bottom": bottom,
                        "left": left,
                    }
                }
        else:
            detection = {
                "name": "Unknown",
                "matched": False,
                "face_locations": {
                    "top": top,
                    "right": right,
                    "bottom": bottom,
                    "left": left,
                }
            }

        data.append(detection)
        return data
