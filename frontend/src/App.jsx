import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';

const API_URL = "http://localhost:8000";
const AI_SERVICE_URL = "http://ai-service:5001";

function App() {
  const [prompt, setPrompt] = useState('');
  const [platform, setPlatform] = useState('Twitter');
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [rotation, setRotation] = useState(0);

  const generatePost = async () => {
    setLoading(true);
    try {
      const res = await axios.post(`${API_URL}/generate`, { prompt, platform });
      setPosts([...posts, res.data]);
    } catch (error) {
      console.error("Error generating post:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (loading) {
      const interval = setInterval(() => {
        setRotation((prevRotation) => (prevRotation + 10) % 360);
      }, 100);

      return () => clearInterval(interval);
    }
  }, [loading]);

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>Social Media Post Generator</h1>
      <div style={styles.form}>
        <input 
          style={styles.input} 
          value={prompt} 
          onChange={e => setPrompt(e.target.value)} 
          placeholder="Enter your prompt"
        />
        <select 
          style={styles.select} 
          value={platform} 
          onChange={e => setPlatform(e.target.value)}
        >
          <option>Twitter</option>
          <option>Facebook</option>
          <option>Instagram</option>
          <option>LinkedIn</option>
        </select>
        <button style={styles.button} onClick={generatePost} disabled={loading}>
          {loading ? 'Generating...' : 'Generate'}
        </button>
      </div>

      <h2 style={styles.postsHeader}>Generated Posts</h2>
      
      {loading ? (
        <div
          style={{
            ...styles.loader,
            transform: `rotate(${rotation}deg)`,
          }}
        />
      ) : (
        <ul style={styles.postsList}>
          {posts.map(p => (
            <li key={p.id} style={styles.postItem}>
              <h3 style={styles.postTitle}>
                {p.platform}:
              </h3>
              <div style={styles.postContent}>
                <ReactMarkdown>{p.content}</ReactMarkdown>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    backgroundColor: '#f4f4f9',
    padding: '2rem',
    borderRadius: '8px',
    boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
    maxWidth: '800px',
    margin: 'auto',
    marginTop: '2rem',
  },
  header: {
    textAlign: 'center',
    color: '#333',
    marginBottom: '1rem',
    fontSize: '2rem',
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '1rem',
    marginBottom: '2rem',
  },
  input: {
    padding: '0.75rem',
    fontSize: '1rem',
    borderRadius: '5px',
    border: '1px solid #ccc',
    outline: 'none',
    width: '100%',
    boxSizing: 'border-box',
  },
  select: {
    padding: '0.75rem',
    fontSize: '1rem',
    borderRadius: '5px',
    border: '1px solid #ccc',
    outline: 'none',
    width: '100%',
    boxSizing: 'border-box',
  },
  button: {
    padding: '0.75rem',
    fontSize: '1rem',
    color: '#fff',
    backgroundColor: '#007bff',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  postsHeader: {
    textAlign: 'center',
    color: '#333',
    fontSize: '1.5rem',
    marginBottom: '1rem',
  },
  postsList: {
    listStyleType: 'none',
    paddingLeft: '0',
    margin: '0',
  },
  postItem: {
    backgroundColor: '#fff',
    padding: '1rem',
    marginBottom: '1rem',
    borderRadius: '5px',
    boxShadow: '0 2px 4px rgba(0, 0, 0, 0.1)',
    borderLeft: '5px solid #007bff',
  },
  postTitle: {
    fontSize: '1.25rem',
    fontWeight: 'bold',
    color: '#333',
  },
  postContent: {
    marginTop: '0.5rem',
    fontSize: '1rem',
    lineHeight: '1.5',
    color: '#555',
  },
  loader: {
    width: '50px',
    height: '50px',
    border: '5px solid #f3f3f3',
    borderTop: '5px solid #007bff',
    borderRadius: '50%',
    margin: 'auto',
  },
};

export default App;
