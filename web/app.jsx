import React, { useState } from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  const [query, setQuery] = useState('');

      const [results, setResults] = useState([]);
  const handleSearch = () => {         fetch(`/search?query=${encodeURIComponent(query)}`)
      .then((res) => res.json())
      .then((data) => setResults(data.results))
      .catch((err) => console.error(err));
    
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
           <ul>
             {results.map((item, i) => (
               <li key={i}>{item.title || JSON.stringify(item)}</li>
             ))}
           </ul>
      </div>
    </div>
  );
}

const root = ReactDOM.createRoot(document.getElementById('root'));

  
