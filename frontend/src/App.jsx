import { useState, useEffect } from 'react'

function App() {
  const [message, setMessage] = useState('Cargando...')
  const [status, setStatus] = useState('loading')

  useEffect(() => {
    fetch('http://localhost:5000/api/hello')
      .then(response => {
        if (!response.ok) {
          throw new Error('Error en la respuesta del servidor')
        }
        return response.json()
      })
      .then(data => {
        setMessage(data.message)
        setStatus('success')
      })
      .catch(error => {
        console.error('Error:', error)
        setMessage('Error al conectar con el backend')
        setStatus('error')
      })
  }, [])

  return (
    <div style={{ textAlign: 'center', marginTop: '50px', fontFamily: 'Arial, sans-serif' }}>
      <h1>Mini SaaS - Gestión de Tareas</h1>
      
      <div style={{ 
        margin: '20px auto', 
        padding: '20px', 
        maxWidth: '500px',
        border: '1px solid #ccc', 
        borderRadius: '8px',
        boxShadow: '0 2px 4px rgba(0,0,0,0.1)'
      }}>
        <h2>Estado del Backend</h2>
        
        {status === 'loading' && (
          <div style={{ color: '#f39c12' }}>
            ⏳ Conectando con el backend...
          </div>
        )}
        
        {status === 'success' && (
          <div style={{ color: '#2ecc71' }}>
            ✅ Conexión exitosa con el backend
            <p style={{ fontWeight: 'bold', marginTop: '10px' }}>
              Mensaje recibido: "{message}"
            </p>
          </div>
        )}
        
        {status === 'error' && (
          <div style={{ color: '#e74c3c' }}>
            ❌ Error de conexión
            <p>No se pudo establecer conexión con el backend</p>
          </div>
        )}
      </div>
      
      <div style={{ 
        margin: '20px auto', 
        padding: '15px', 
        maxWidth: '500px',
        backgroundColor: '#f8f9fa', 
        borderRadius: '8px',
        fontSize: '14px',
        color: '#555'
      }}>
        <p>Esta es una aplicación de ejemplo que muestra la comunicación entre React (frontend) y Flask (backend).</p>
      </div>
    </div>
  )
}

export default App
