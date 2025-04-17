# coordinator/task_registry.py - Registro de tareas en Redis 

import redis, json, time

r = redis.Redis(host="localhost", port=6379, db=0)

def save_task(task: dict):
    task_key = f"tarea:{task['task_id']}"
    task_data = {
        **task,
        "status": "pendiente",
        "timestamp": time.time(),
        "reason": ""
    }
    r.set(task_key, json.dumps(task_data))

def get_all_tasks():
    keys = r.keys("tarea:*")
    tasks = []
    for k in keys:
        raw = r.get(k)
        if raw:
            try:
                tasks.append(json.loads(raw))
            except Exception as e:
                print(f"⚠️ Error al leer tarea {k}: {e}")
    return tasks

def get_pending_tasks_by_node(node_id):
    return [t for t in get_all_tasks() if t.get("assigned_to") == node_id and t.get("status") == "pendiente"]

def update_task(task_id, updates):
    task_key = f"tarea:{task_id}"
    raw = r.get(task_key)
    if not raw:
        print(f"⚠️ No se encontró la tarea {task_id} para actualizar.")
        return
    data = json.loads(raw)
    data.update(updates)
    r.set(task_key, json.dumps(data))
    print(f"✅ Tarea {task_id} actualizada: {updates}")

