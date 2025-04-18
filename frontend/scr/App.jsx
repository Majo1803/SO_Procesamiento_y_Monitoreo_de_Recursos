import React from 'react'
import NodesView from './pages/NodesView'

function App() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-md p-4 text-xl font-bold text-center">
        📊 Distributed Task Dashboard
      </header>
      <main>
        <NodesView />
      </main>
    </div>
  )
}

export default App
