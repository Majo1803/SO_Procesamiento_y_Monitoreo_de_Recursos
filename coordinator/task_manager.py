# coordinator/task_manager.py

import os, base64, uuid, json, time, redis, random
import requests

from coordinator.task_registry import save_task 

IMAGES_FOLDER = "images"
NODES_API = "http://localhost:8000/api/nodes"

r = redis.Redis(host="localhost", port=6379, db=0)

def encode_image(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def get_least_loaded_node():
    try:
        res = requests.get(NODES_API, timeout=2)
        nodes = res.json()
        # Ordenar por suma CPU + RAM (puede personalizarse)
        nodes.sort(key=lambda n: n["cpu"] + n["ram"])
        return nodes[0]["node_id"] if nodes else None
    except Exception as e:
        print("❌ Error consultando nodos:", e)
        return None

def assign_task(image_path):
    task_type = random.choice(["face_detection", "classification"])
    task_id = str(uuid.uuid4())
    encoded = encode_image(image_path)

    node_id = get_least_loaded_node()
    if not node_id:
        print("⚠️ No se encontró nodo disponible.")
        return

    task = {
        "task_id": task_id,
        "type": task_type,
        "filename": os.path.basename(image_path),
        "image_base64": encoded
    }

    channel = f"tareas_{node_id}"
    save_task(task)  # Guardar la tarea en Redis
    r.publish(channel, json.dumps(task))  # Luego publicarla al nodo correspondiente
    print(f"📦 Tarea {task_id} enviada a {node_id} ({task_type})")

def enviar_todas():
    for fname in os.listdir(IMAGES_FOLDER):
        if fname.lower().endswith((".jpg", ".png", ".jpeg")):
            assign_task(os.path.join(IMAGES_FOLDER, fname))
            time.sleep(1)  # para simular tráfico real

if __name__ == "__main__":
    enviar_todas()
