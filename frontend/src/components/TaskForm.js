import React, { useState, useEffect } from 'react';
import axios from 'axios';

const TaskForm = ({ token, task, onTaskCreated, onTaskUpdated }) => {
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState('Medium');
  const [complexity, setComplexity] = useState('Medium');
  const [dueDate, setDueDate] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (task) {
      setTitle(task.title);
      setDescription(task.description);
      setPriority(task.priority);
      setComplexity(task.complexity);
      setDueDate(task.due_date);
    } else {
      setTitle('');
      setDescription('');
      setPriority('Medium');
      setComplexity('Medium');
      setDueDate('');
    }
  }, [task]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    const taskData = { title, description, priority, complexity, due_date: dueDate };
    try {
      if (task) {
        await axios.put(`/tasks/${task.id}`, taskData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        onTaskUpdated();
      } else {
        await axios.post('/tasks', taskData, {
          headers: { Authorization: `Bearer ${token}` }
        });
        onTaskCreated();
        setTitle('');
        setDescription('');
        setPriority('Medium');
        setComplexity('Medium');
        setDueDate('');
      }
    } catch (error) {
      setError('Failed to save task');
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h3>{task ? 'Edit Task' : 'Create Task'}</h3>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <div>
        <label>Title:</label>
        <input type="text" value={title} onChange={(e) => setTitle(e.target.value)} required />
      </div>
      <div>
        <label>Description:</label>
        <textarea value={description} onChange={(e) => setDescription(e.target.value)}></textarea>
      </div>
      <div>
        <label>Urgency:</label>
        <select value={priority} onChange={(e) => setPriority(e.target.value)}>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>
      <div>
        <label>Complexity:</label>
        <select value={complexity} onChange={(e) => setComplexity(e.target.value)}>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
      </div>
      <div>
        <label>Due Date:</label>
        <input type="date" value={dueDate} onChange={(e) => setDueDate(e.target.value)} />
      </div>
      <button type="submit" disabled={loading}>{loading ? (task ? 'Updating...' : 'Creating...') : (task ? 'Update Task' : 'Create Task')}</button>
    </form>
  );
};

export default TaskForm;