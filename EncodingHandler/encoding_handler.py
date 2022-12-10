import pickle

import cv2
import face_recognition


class FaceEncoding:
    @staticmethod
    def get_face_encoding(*image_paths: str) -> bytes:
        """
        Method for getting embedding of faces from images

        :param image_paths: str, paths to the images
        :return: bytes, serialized embedding of faces from images
        """
        encodings = []

        for image_path in image_paths:
            image = cv2.imread(image_path)
            rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            encodings.extend(face_recognition.face_encodings(rgb, face_recognition.face_locations(rgb, model='hog')))
        return pickle.dumps(encodings)
