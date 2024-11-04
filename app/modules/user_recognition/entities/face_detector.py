import typing as t

import face_recognition
from numpy import ndarray, float64
import cv2.typing

from app.modules.common import interfaces


class FaceDetector(interfaces.Detector):

    def load_image(self, frame: cv2.typing.MatLike) -> ndarray[t.Any]:
        return face_recognition.load_image_file(frame)

    def get_face_locations(self, frame: cv2.typing.MatLike) -> t.List[t.Tuple[int, t.Any, t.Any, int]]:
        return face_recognition.face_locations(frame)

    def get_face_encodings(
        self,
        frame: cv2.typing.MatLike,
        locations: t.List[t.Tuple[int, t.Any, t.Any, int]] | None = None
    ) -> t.List[ndarray]:

        return face_recognition.face_encodings(frame, locations)

    def compare_faces(
        self,
        know_encodings: t.List[ndarray],
        unknow_encoding: t.List[ndarray]
    ) -> t.List[t.Any]:

        return face_recognition.compare_faces(know_encodings, unknow_encoding)

    def get_face_distances(
        self,
        know_encodings: t.List[ndarray],
        unknow_encoding: t.List[ndarray]
    ) -> (ndarray[float64] | t.Any):

        return face_recognition.face_distance(know_encodings, unknow_encoding)