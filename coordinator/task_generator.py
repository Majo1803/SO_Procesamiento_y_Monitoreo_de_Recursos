# coordinator/task_generator.py

import os
import base64
import uuid
import redis
import json
import random

IMAGES_FOLDER = "images"
TASK_CHANNEL = "tareas_distribuidas"

r = redis.Redis(host="localhost", port=6379, db=0)

def encode_image_to_base64(path):
    with open(path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode("utf-8")

def create_task_payload(image_path, task_type):
    return {
        "task_id": str(uuid.uuid4()),
        "type": task_type,
        "filename": os.path.basename(image_path),
        "image_base64": encode_image_to_base64(image_path)
    }

def generate_and_publish_tasks():
    for filename in os.listdir(IMAGES_FOLDER):
        if filename.lower().endswith((".jpg", ".jpeg", ".png")):
            full_path = os.path.join(IMAGES_FOLDER, filename)
            task_type = random.choice(["face_detection", "classification"])
            task = create_task_payload(full_path, task_type)
            r.publish(TASK_CHANNEL, json.dumps(task))
            print(f"Tarea enviada: {task['task_id']} - {filename} ({task_type})")

if __name__ == "__main__":
    generate_and_publish_tasks()
