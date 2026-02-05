import React from 'react';

// React app disabled - redirecting to fox3d.html
function App() {
  React.useEffect(() => {
    window.location.href = '/fox3d.html';
  }, []);

  return (
    <div style={{
      width: '100vw',
      height: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      color: 'white',
      fontSize: '2rem'
    }}>
      <div>
        <div style={{ fontSize: '5rem', marginBottom: '20px' }}>🦊</div>
        <p>در حال انتقال به رابط سه‌بعدی...</p>
      </div>
    </div>
  );
}

export default App;