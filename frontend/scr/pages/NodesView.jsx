import React, { useEffect, useState } from 'react'
import NodeCard from '../components/NodeCard'

const NodesView = () => {
  const [nodes, setNodes] = useState([])

  const fetchNodes = async () => {
    try {
      const res = await fetch('http://localhost:8000/api/nodes')
      const data = await res.json()
      setNodes(data)
    } catch (err) {
      console.error("Error al cargar nodos:", err)
    }
  }

  useEffect(() => {
    fetchNodes()
    const interval = setInterval(fetchNodes, 2000)
    return () => clearInterval(interval)
  }, [])

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">🖥️ Nodos Activos</h1>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {nodes.map((node) => (
          <NodeCard key={node.node_id} node={node} />
        ))}
      </div>
    </div>
  )
}

export default NodesView
