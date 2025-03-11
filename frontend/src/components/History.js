import React from 'react';

const History = ({ history, setHistory }) => {
  const deleteItem = (index) => {
    const newHistory = history.filter((_, i) => i !== index);
    setHistory(newHistory);
  };

  const clearHistory = () => {
    setHistory([]);
  };

  return (
    <div className="history">
      <h3>Advice History</h3>
      {history.length === 0 && <p>No history yet.</p>}
      {history.map((item, index) => (
        <div key={index} className="history-item">
          <strong>{item.timestamp} - {item.task}</strong>
          <pre>{item.query}</pre>
          <pre>{item.response}</pre>
          <button onClick={() => deleteItem(index)}>Delete</button>
        </div>
      ))}
      {history.length > 0 && (
        <button onClick={clearHistory} style={{ marginTop: '1rem' }}>
          Clear All History
        </button>
      )}
    </div>
  );
};

export default History;
