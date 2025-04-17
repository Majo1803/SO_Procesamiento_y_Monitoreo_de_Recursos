# main.py - servidor de monitoreo que recibe datos de los nodos y los almacena en Redis 
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis import Redis
import threading, json
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.models import NodeStatus


app = FastAPI()
r = Redis(host="localhost", port=6379, db=0)
nodes_data = {}

# Permitir dashboard externo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/nodes")
def get_nodes():
    return list(nodes_data.values())

def redis_listener():
    pubsub = r.pubsub()
    pubsub.subscribe("nodo_monitoring")
    for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            nodes_data[data["node_id"]] = data

if __name__ == "__main__":
    threading.Thread(target=redis_listener, daemon=True).start()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
