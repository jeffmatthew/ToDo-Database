import React, { useState } from 'react';
import './App.css';
import Header from './components/Header';
import TodoList from './components/TodoList';
import FilterButtons from './components/FilterButtons';
import { auth } from './firebase';

function App() {
  const [user, setUser] = useState(null);
  const [tasks, setTasks] = useState([]);
  const [inputValue, setInputValue] = useState('');

  const handleInputChange = (e) => {
    setInputValue(e.target.value);
  };

  const handleAddTask = () => {
    if (inputValue.trim() !== '') {
      setTasks([...tasks, { id: Date.now(), text: inputValue, completed: false }]);
      setInputValue('');
    }
  };

  const toggleTask = (id) => {
    setTasks(tasks.map(task => {
      if (task.id === id) {
        return { ...task, completed: !task.completed };
      }
      return task;
    }));
  };

  const handleFilter = (filter) => {
    switch (filter) {
      case 'all':
        setFilteredTasks(tasks);
        break;
      case 'active':
        setFilteredTasks(tasks.filter(task => !task.completed));
        break;
      case 'completed':
        setFilteredTasks(tasks.filter(task => task.completed));
        break;
      default:
        break;
    }
  };

  const handleSignIn = async () => {
    try {
      const provider = new firebase.auth.GoogleAuthProvider();
      await auth.signInWithPopup(provider);
    } catch (error) {
      console.error(error);
    }
  };

  const handleSignOut = async () => {
    try {
      await auth.signOut();
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div className="App">
      <Header user={user} handleSignIn={handleSignIn} handleSignOut={handleSignOut} />
      <div className="input-container">
        <input
          type="text"
          value={inputValue}
          onChange={handleInputChange}
          placeholder="Add a new task..."
        />
        <button onClick={handleAddTask}>Add</button>
      </div>
      <TodoList tasks={tasks} toggleTask={toggleTask} />
      <FilterButtons handleFilter={handleFilter} />
    </div>
  );
}

export default App;
