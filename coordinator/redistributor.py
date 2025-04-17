# coordinator/redistributor.py - Redistribuidor de tareas en caso de saturación de nodos 
# coordinator/redistributor.py

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import time
import requests
import redis
import json
from task_registry import get_pending_tasks_by_node, update_task, save_task

r = redis.Redis(host="localhost", port=6379, db=0)
NODES_API = "http://localhost:8000/api/nodes"

def get_saturated_nodes():
    try:
        res = requests.get(NODES_API, timeout=2)
        nodes = res.json()
        return [n["node_id"] for n in nodes if n["cpu"] > 85 or n["ram"] > 85]
    except Exception as e:
        print("❌ Error consultando nodos:", e)
        return []
    except requests.exceptions.RequestException as e:
        print(f"❌ Error consultando nodos: {e}")
        return []


def get_least_loaded_node(exclude_ids=[]):
    try:
        res = requests.get(NODES_API)
        nodes = [n for n in res.json() if n["node_id"] not in exclude_ids]
        nodes.sort(key=lambda x: x["cpu"] + x["ram"])
        return nodes[0]["node_id"] if nodes else None
    except Exception as e:
        print("❌ Error obteniendo nodo más libre:", e)
        return None

def redistribute():
    saturated_nodes = get_saturated_nodes()
    if not saturated_nodes:
        return

    print(f"⚠️ Detectados nodos saturados: {saturated_nodes}")

    for nodo in saturated_nodes:
        pendientes = get_pending_tasks_by_node(nodo)
        print(f"🔍 Nodo {nodo} tiene {len(pendientes)} tareas pendientes")

        for tarea in pendientes:
            nuevo_nodo = get_least_loaded_node(exclude_ids=[nodo])
            if not nuevo_nodo:
                print("⚠️ No hay nodos disponibles para redistribuir")
                continue

            # Actualizar Redis con nueva asignación
            update_task(tarea["task_id"], {
                "assigned_to": nuevo_nodo,
                "reason": f"Redistribuida desde {nodo} por saturación"
            })

            # Publicar al nuevo nodo
            tarea["assigned_to"] = nuevo_nodo
            canal = f"tareas_{nuevo_nodo}"
            r.publish(canal, json.dumps(tarea))
            print(f"🔁 Tarea {tarea['task_id']} reasignada de {nodo} a {nuevo_nodo}")

if __name__ == "__main__":
    print("♻️ Redistribuidor automático iniciado...")
    while True:
        redistribute()
        time.sleep(5)
