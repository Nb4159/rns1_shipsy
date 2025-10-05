import React, { useState } from 'react';
import axios from 'axios';
import TaskForm from './TaskForm';
import './TaskList.css';

const TaskList = ({ token, tasks, fetchTasks }) => {
  const [editingTask, setEditingTask] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [overdueFilter, setOverdueFilter] = useState(false);
  const [urgencyFilter, setUrgencyFilter] = useState('');
  const [complexityFilter, setComplexityFilter] = useState('');

  const handleDelete = async (taskId) => {
    if (window.confirm('Are you sure you want to delete this task?')) {
      setLoading(true);
      setError(null);
      try {
        await axios.delete(`http://127.0.0.1:5000/tasks/${taskId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        fetchTasks();
      } catch (error) {
        setError('Failed to delete task');
      } finally {
        setLoading(false);
      }
    }
  };

  const handleEdit = (task) => {
    setEditingTask(task);
  };

  const handleUpdate = () => {
    setEditingTask(null);
    fetchTasks();
  }

  const handleFilter = (e) => {
    e.preventDefault();
    console.log('handleFilter called');
    const options = {};
    if (overdueFilter) {
      options.overdue = overdueFilter;
    }
    if (urgencyFilter) {
      options.urgency = urgencyFilter;
    }
    if (complexityFilter) {
      options.complexity = complexityFilter;
    }
    fetchTasks(options);
  }

  return (
    <div>
      <h2>Task List</h2>
      <form onSubmit={handleFilter} className="filter-form">
        <label>
          <input type="checkbox" checked={overdueFilter} onChange={(e) => setOverdueFilter(e.target.checked)} />
          Overdue
        </label>
        <select value={urgencyFilter} onChange={(e) => setUrgencyFilter(e.target.value)}>
          <option value="">All Urgencies</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
        <select value={complexityFilter} onChange={(e) => setComplexityFilter(e.target.value)}>
          <option value="">All Complexities</option>
          <option value="Low">Low</option>
          <option value="Medium">Medium</option>
          <option value="High">High</option>
        </select>
        <button type="submit">Filter</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>}
      {loading && <p>Loading...</p>}
      <ul className="task-list">
        {tasks.map(task => (
          <li key={task.id} className={`task-card ${task.completed ? 'completed' : ''}`}>
            <h3>{task.title}</h3>
            <p>{task.description}</p>
            <p>Urgency: {task.priority}</p>
            <p>Complexity: {task.complexity}</p>
            <p>Due Date: {task.due_date}</p>
            <p>Overdue: {task.is_overdue ? 'Yes' : 'No'}</p>
            <div className="actions">
              <button onClick={() => handleEdit(task)}>Edit</button>
              <button onClick={() => handleDelete(task.id)} disabled={loading}>Delete</button>
            </div>
          </li>
        ))}
      </ul>
      {editingTask && (
        <TaskForm
          token={token}
          task={editingTask}
          onTaskUpdated={handleUpdate}
        />
      )}
    </div>
  );
};

export default TaskList;