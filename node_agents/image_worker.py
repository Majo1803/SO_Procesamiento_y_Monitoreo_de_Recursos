# node_agents/image_worker.py

import os
import sys

# Agregar la raíz del proyecto al path para importar 'tasks'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import redis
import json
import time
from tasks.classification import classify_image
from tasks.face_detection import detect_faces

NODE_ID = "nodo_imagen_1"
RESULTS_FOLDER = "results"

os.makedirs(RESULTS_FOLDER, exist_ok=True)

def save_result(task_id, result, original_filename, task_type):
    filename = f"resultado_{task_type}_{task_id}.json"
    path = os.path.join(RESULTS_FOLDER, filename)
    data = {
        "task_id": task_id,
        "task_type": task_type,
        "node_id": NODE_ID,
        "original_filename": original_filename,
        "result": result,
        "timestamp": time.time()
    }
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
    print(f"[{NODE_ID}] Resultado guardado en {path}")

def handle_task(task):
    task_id = task.get("task_id")
    task_type = task.get("type")
    filename = task.get("filename", "sin_nombre.jpg")
    image_b64 = task.get("image_base64")

    print(f"[{NODE_ID}] Ejecutando tarea {task_id} ({task_type}) sobre {filename}...")

    try:
        if task_type == "face_detection":
            result = detect_faces(image_b64)
        elif task_type == "classification":
            result = classify_image(image_b64)
        else:
            print(f"[{NODE_ID}] Tipo de tarea desconocido: {task_type}")
            return

        print(f"[{NODE_ID}] Resultado tarea {task_id}: {result}")
        save_result(task_id, result, filename, task_type)

    except Exception as e:
        print(f"[{NODE_ID}] Error ejecutando tarea {task_id}: {e}")

def start_worker():
    r = redis.Redis(host="localhost", port=6379, db=0)
    pubsub = r.pubsub()
    TASK_CHANNEL = f"tareas_{NODE_ID}"
    pubsub.subscribe(TASK_CHANNEL)


    print(f"[{NODE_ID}] Esperando tareas en Redis...")
    for message in pubsub.listen():
        if message["type"] != "message":
            continue

        try:
            task = json.loads(message["data"])
            handle_task(task)
        except Exception as e:
            print(f"[{NODE_ID}] Error procesando mensaje: {e}")

if __name__ == "__main__":
    start_worker()
