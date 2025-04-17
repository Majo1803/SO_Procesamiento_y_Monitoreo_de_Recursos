# tasks/classification.py

import torch
import torchvision.transforms as transforms
from torchvision.models import mobilenet_v2
from PIL import Image
import base64
from io import BytesIO

# Mapeo simplificado a 5 categorías (puede ajustarse según resultados)
CATEGORY_MAP = {
    # Animales
    "dog": "Perro",
    "puppy": "Perro",
    "retriever": "Perro",
    "terrier": "Perro",
    "hound": "Perro",
    "shepherd": "Perro",
    
    "cat": "Gato",
    "tabby": "Gato",
    "kitten": "Gato",
    "persian": "Gato",

    # Personas / Retratos
    "person": "Retrato",
    "man": "Retrato",
    "woman": "Retrato",
    "face": "Retrato",
    "wig": "Retrato",
    "mask": "Retrato",

    # Vehículos
    "car": "Vehículo",
    "truck": "Vehículo",
    "automobile": "Vehículo",
    "jeep": "Vehículo",
    "bus": "Vehículo",
    "motorcycle": "Vehículo",

    # Paisajes y naturaleza
    "beach": "Paisaje",
    "sandbar": "Paisaje",
    "cliff": "Paisaje",
    "valley": "Paisaje",
    "mountain": "Paisaje",
    "landscape": "Paisaje",
    "lakeside": "Paisaje",
    "forest": "Paisaje",
    "field": "Paisaje",
    "desert": "Paisaje",
}


# Modelo MobileNetV2 preentrenado
model = mobilenet_v2(pretrained=True)
model.eval()

# Transformaciones para entrada de imagen
transform = transforms.Compose([
    transforms.Resize(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406],
                         std=[0.229, 0.224, 0.225])
])

# Cargar etiquetas de ImageNet
LABELS_URL = "https://raw.githubusercontent.com/pytorch/hub/master/imagenet_classes.txt"
imagenet_labels = None
if imagenet_labels is None:
    import requests
    imagenet_labels = requests.get(LABELS_URL).text.splitlines()

def decode_image(base64_str):
    image_data = base64.b64decode(base64_str)
    return Image.open(BytesIO(image_data)).convert("RGB")

def classify_image(base64_image: str):
    img = decode_image(base64_image)
    input_tensor = transform(img).unsqueeze(0)
    with torch.no_grad():
        output = model(input_tensor)
        probs = torch.nn.functional.softmax(output[0], dim=0)
        top_idx = torch.argmax(probs).item()
        label = imagenet_labels[top_idx]
        confidence = probs[top_idx].item()

        # Buscar una categoría simplificada
        simplified = "Desconocido"
        for keyword, category in CATEGORY_MAP.items():
            if keyword.lower() in label.lower():
                simplified = category
                break

    return {
        "label": label,
        "confidence": round(confidence, 4),
        "category": simplified
    }
