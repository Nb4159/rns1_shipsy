import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import axios from 'axios';
import Login from './components/Login';
import Register from './components/Register';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import './App.css';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchOptions, setSearchOptions] = useState({});

  const handleSetToken = (newToken) => {
    setToken(newToken);
    localStorage.setItem('token', newToken);
  };

  const handleLogout = () => {
    setToken(null);
    localStorage.removeItem('token');
  };

  axios.interceptors.response.use(response => {
    return response;
  }, error => {
    if (error.response.status === 401) {
      handleLogout();
    }
    return Promise.reject(error);
  });

  const fetchTasks = async (options = {}) => {
    console.log('fetchTasks called with:', options);
    setLoading(true);
    setError(null);
    try {
      const response = await axios.get('http://127.0.0.1:5000/tasks', {
        headers: { Authorization: `Bearer ${token}` },
        params: options
      });
      setTasks(response.data.tasks);
    } catch (err) {
      setError('Failed to fetch tasks');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (options) => {
    console.log('handleSearch called with:', options);
    setSearchOptions({...options});
  }

  useEffect(() => {
    if (token) {
      fetchTasks();
    }
  }, [token, searchOptions]);

  return (
    <Router>
      <div className="App">
        <header className="App-header">
          <h1>Task Management</h1>
          {token && <button onClick={handleLogout}>Logout</button>}
        </header>
        <main>
          {loading && <p>Loading...</p>}
          {error && <p style={{ color: 'red' }}>{error}</p>}
          <Routes>
            <Route path="/login" element={<Login setToken={handleSetToken} />} />
            <Route path="/register" element={<Register />} />
            <Route path="/" element={token ? (
              <div>
                <TaskForm token={token} onTaskCreated={fetchTasks} onTaskUpdated={fetchTasks} />
                <TaskList 
                  token={token} 
                  tasks={tasks} 
                  fetchTasks={fetchTasks} 
                  handleSearch={handleSearch} 
                />
              </div>
            ) : (
              <Navigate to="/login" />
            )} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;