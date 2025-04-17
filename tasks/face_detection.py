# tasks/face_detection.py

import cv2
import numpy as np
import base64
from io import BytesIO
from PIL import Image

# Cargar el modelo Haar Cascade preentrenado para detección facial
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

def decode_image(base64_str: str) -> np.ndarray:
    """Convierte una imagen en base64 a un array de OpenCV"""
    image_data = base64.b64decode(base64_str)
    image = Image.open(BytesIO(image_data)).convert("RGB")
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def detect_faces(base64_image: str):
    """Devuelve una lista de rectángulos de rostros detectados"""
    img = decode_image(base64_image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    results = []
    for (x, y, w, h) in faces:
        results.append({"x": int(x), "y": int(y), "w": int(w), "h": int(h)})

    return {
        "face_count": len(results),
        "faces": results
    }
