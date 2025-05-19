import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [query, setQuery] = useState('');

  const handleSearch = () => {
    alert(`Searching for ${query}`);
    // TODO: call /search API when ready
  };

  return (
    <div style={{ fontFamily: 'sans-serif', padding: '2rem' }}>
      <h1>BeatVector™ Hip-Hop Search</h1>
      <div style={{ marginTop: '1rem' }}>
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search term..."
          style={{ padding: '0.5rem', width: '300px' }}
        />
        <button
          onClick={handleSearch}
          style={{ padding: '0.5rem 1rem', marginLeft: '0.5rem' }}
        >
          Search
        </button>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<App />);
