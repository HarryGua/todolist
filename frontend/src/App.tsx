import React, { useState, useEffect } from 'react';
import { api } from './services/api';
import type { TodoItem } from './services/api';
import './App.css';

function App() {
  const [todos, setTodos] = useState<TodoItem[]>([]);
  const [newTodo, setNewTodo] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadTodos();
  }, []);

  const loadTodos = async () => {
    try {
      const data = await api.getTodos();
      setTodos(data);
    } catch (error) {
      console.error('Error loading todos:', error);
    } finally {
      setLoading(false);
    }
  };

  const addTodo = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!newTodo.trim()) return;

    try {
      const todo = await api.createTodo({
        title: newTodo.trim(),
        description: '',
        completed: false,
      });
      setTodos([todo, ...todos]);
      setNewTodo('');
    } catch (error) {
      console.error('Error adding todo:', error);
    }
  };

  const toggleTodo = async (todo: TodoItem) => {
    try {
      const updatedTodo = await api.updateTodo(todo.id!, {
        ...todo,
        completed: !todo.completed,
      });
      setTodos(todos.map(t => t.id === todo.id ? updatedTodo : t));
    } catch (error) {
      console.error('Error updating todo:', error);
    }
  };

  const deleteTodo = async (id: string) => {
    try {
      await api.deleteTodo(id);
      setTodos(todos.filter(t => t.id !== id));
    } catch (error) {
      console.error('Error deleting todo:', error);
    }
  };

  if (loading) {
    return <div className="loading">加载中...</div>;
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>待办事项清单</h1>
      </header>
      
      <main className="app-main">
        <form onSubmit={addTodo} className="todo-form">
          <input
            type="text"
            value={newTodo}
            onChange={(e) => setNewTodo(e.target.value)}
            placeholder="添加新的待办事项..."
            className="todo-input"
          />
          <button type="submit" className="add-button">
            添加
          </button>
        </form>

        <div className="todo-list">
          {todos.length === 0 ? (
            <p className="empty-message">暂无待办事项</p>
          ) : (
            todos.map(todo => (
              <div key={todo.id} className={`todo-item ${todo.completed ? 'completed' : ''}`}>
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => toggleTodo(todo)}
                  className="todo-checkbox"
                />
                <span className="todo-title">{todo.title}</span>
                <button
                  onClick={() => deleteTodo(todo.id!)}
                  className="delete-button"
                >
                  删除
                </button>
              </div>
            ))
          )}
        </div>
      </main>
    </div>
  );
}

export default App;
