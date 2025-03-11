import React, { useState } from 'react';
import Login from './components/Login';
import Sidebar from './components/Sidebar';
import AdviceForm from './components/AdviceForm';
import History from './components/History';
import './App.css';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [selectedTask, setSelectedTask] = useState("generic"); // "generic", "portfolio", "domain"
  const [history, setHistory] = useState([]);

  // When advice is received, save it in history
  const addHistoryItem = (item) => {
    setHistory(prev => [item, ...prev]);
  };

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div className="app-container">
      <Sidebar selectedTask={selectedTask} setSelectedTask={setSelectedTask} setLoggedIn={setLoggedIn} />
      <div className="main-content">
        <header className="hero">
          <div className="hero-overlay"></div>
          <div className="hero-content">
            <h1>Multi-Agent Financial Analyzer</h1>
            <p>Get personalized financial insights with our AI-powered analysis.</p>
          </div>
        </header>
        <div className="content">
          <AdviceForm selectedTask={selectedTask} addHistoryItem={addHistoryItem} />
          <History history={history} setHistory={setHistory} />
        </div>
      </div>
    </div>
  );
}

export default App;