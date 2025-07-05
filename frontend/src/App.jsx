import { useState } from 'react'
import './App.css'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <div>
        <h1>OdontoSoft Frontend</h1>
        <div className="card">
          <button onClick={() => setCount((count) => count + 1)}>
            count is {count}
          </button>
          <p>
            Edite <code>src/App.jsx</code> e salve para testar HMR
          </p>
        </div>
        <p className="read-the-docs">
          Clique nos logos do Vite e React para aprender mais
        </p>
      </div>
    </>
  )
}

export default App
