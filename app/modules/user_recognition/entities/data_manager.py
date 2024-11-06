import os
import csv
import typing as t

from flask import current_app
from numpy import ndarray
import cv2.typing
import cv2

from .face_detector import FaceDetector
from .image_manager import ImageManager
from app.modules.common import interfaces as common_interfaces
from app.modules.user_recognition.models.person import Person
from app.config import db


class DataManager(common_interfaces.Manager):

    def __init__(self, image_manager: ImageManager, face_detector: FaceDetector, path: str | None = None) -> None:
        self._path = path
        self.face_detector = face_detector
        self.image_manager = image_manager

        self._image_names = [f for f in os.listdir(self._path) if os.path.isfile(os.path.join(self._path, f))]
        self._data = []
        self._names = []
        self._encodings = []

        self.set_data()

    def get_image_names(self) -> t.List[str]:
        return self._image_names

    def get_names(self) -> t.List[str]:
        return self._names

    def get_encodings(self) -> t.List[ndarray]:
        return self._encodings

    def get_data(self) -> list:
        return self._data

    def set_data(self) -> None:
        person_data = {}
        csv_file_path = 'person_data.csv'

        with open(csv_file_path, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                image_name = row['image_name']
                person_data[image_name] = row

        with current_app.app_context():
            for image_name in self.get_image_names():
                print(image_name)
                # Verificar si la imagen está en el CSV
                if image_name not in person_data:
                    print(f"La imagen {image_name} no está en el archivo CSV.")
                    continue

                data = person_data[image_name]
                name = data['name']
                image_path = os.path.join(self._path, image_name)
                # print(data)
                # print(image_path)

                if not os.path.isfile(image_path):
                    continue

                # Verificar si ya existe un registro de Person con ese nombre
                person = Person.query.filter_by(name=name).first()

                if person is None:
                    # Procesar la imagen para obtener la codificación facial
                    image = cv2.imread(image_path)
                    if image is None:
                        continue
                    resized_image = self.image_manager.resize_image(image=image, scale_percent=40.0)
                    encodings = self.face_detector.get_face_encodings(resized_image)

                    if encodings:
                        face_encoding = encodings[0]
                        # Crear un nuevo registro de Person con los datos del CSV
                        person = Person(
                            name=data['name'],
                            document_number=data['document_number'],
                            gender=data['gender'],
                            user_type=data['user_type'],
                            dependency=data['dependency'],
                            academic_program=data['academic_program'],
                            face_encoding=face_encoding
                        )
                        db.session.add(person)
                        db.session.commit()

                        self._names.append(person.name)
                        self._encodings.append(face_encoding)
                        self._data.append({
                            "name": person.name,
                            "encoding": face_encoding,
                        })
                    else:
                        print(f"No se detectó ninguna cara en la imagen {image_name}")
                else:
                    # Si la persona ya existe, agregar sus datos
                    self._names.append(person.name)
                    self._encodings.append(person.face_encoding)
                    self._data.append({
                        "name": person.name,
                        "encoding": person.face_encoding,
                    })

    def set_encodings(self) -> t.List[ndarray]:
        for image_name in self.get_image_names():
            image_path = os.path.join(self._path, image_name)
            if not os.path.isfile(image_path):
                continue

            image = cv2.imread(image_path)
            if image is None:
                continue

            resized_image = self.image_manager.resize_image(image=image, scale_percent=40.0)
            encodings = self.face_detector.get_face_encodings(resized_image)

            if encodings:
                self._encodings.append(encodings[0])
            else:
                pass

        return self._encodings


    def set_names(self) -> t.List[str]:
        self._names = [
            image_name.split('.')[0]
            for image_name in self.get_image_names()
        ]

        return self._names
