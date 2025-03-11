import React from 'react';

const Sidebar = ({ selectedTask, setSelectedTask, setLoggedIn }) => {
  return (
    <div className="sidebar">
      <h2>Navigation</h2>
      <button
        className={selectedTask === "generic" ? "active" : ""}
        onClick={() => setSelectedTask("generic")}
      >
        Generic Advice
      </button>
      <button
        className={selectedTask === "portfolio" ? "active" : ""}
        onClick={() => setSelectedTask("portfolio")}
      >
        Portfolio Management
      </button>
      <button
        className={selectedTask === "domain" ? "active" : ""}
        onClick={() => setSelectedTask("domain")}
      >
        Domain-Specific Advice
      </button>
      <button className="logout" onClick={() => setLoggedIn(false)}>
        Logout
      </button>
    </div>
  );
};

export default Sidebar;