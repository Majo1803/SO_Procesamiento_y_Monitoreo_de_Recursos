import React from 'react'

const NodeCard = ({ node }) => {
  const isSaturated = node.cpu > 85 || node.ram > 85

  return (
    <div className={`rounded-xl p-4 border shadow-md transition-all duration-300
      ${isSaturated ? 'bg-red-100 border-red-400' : 'bg-white border-gray-200'}`}>
      <h3 className="text-lg font-semibold">{node.node_id}</h3>
      <p className="text-sm text-gray-500">{node.hostname}</p>
      <div className="mt-2 space-y-1">
        <p>🧠 CPU: <span className={node.cpu > 85 ? 'text-red-600 font-bold' : ''}>{node.cpu}%</span></p>
        <p>💾 RAM: <span className={node.ram > 85 ? 'text-red-600 font-bold' : ''}>{node.ram}%</span></p>
        <p>🗃️ Disco: {node.disk}%</p>
        <p>🌐 Red: {(node.network / 1_000_000).toFixed(2)} MB</p>
      </div>
    </div>
  )
}

export default NodeCard
