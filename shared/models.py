# Este código define un modelo de datos para representar el estado de un nodo en un sistema distribuido.
# El modelo incluye información sobre el ID del nodo, el nombre de host, el uso de CPU, RAM, disco y red, así como una marca de tiempo.
from pydantic import BaseModel

class NodeStatus(BaseModel):
    node_id: str
    hostname: str
    cpu: float
    ram: float
    disk: float
    network: float
    timestamp: float

