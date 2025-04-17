# agent1.py - simulacion de un nodo de monitoreo en una computadora
import psutil
import time
import redis
import json
import socket

NODE_ID = "nodo_1"
r = redis.Redis(host="localhost", port=6379, db=0)

def get_resource_data():
    return {
        "node_id": NODE_ID,
        "hostname": socket.gethostname(),
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage('/').percent,
        "network": psutil.net_io_counters().bytes_sent + psutil.net_io_counters().bytes_recv,
        "timestamp": time.time()
    }

if __name__ == "__main__":
    print(f"[{NODE_ID}] Iniciando agente de monitoreo...")
    while True:
        data = get_resource_data()
        r.publish("nodo_monitoring", json.dumps(data))
        time.sleep(2)
