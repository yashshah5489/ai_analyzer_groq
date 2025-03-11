import React, { useState } from 'react';
import axios from 'axios';

const AdviceForm = ({ selectedTask, addHistoryItem }) => {
  // Common form fields
  const [userInput, setUserInput] = useState("");
  const [additionalContextQuery, setAdditionalContextQuery] = useState("");
  const [temperature, setTemperature] = useState(0.7);
  const [maxTokens, setMaxTokens] = useState(1024);
  // Task-specific fields
  const [portfolioDetails, setPortfolioDetails] = useState("");
  const [domainType, setDomainType] = useState("Tech Stocks");
  const [domainDetails, setDomainDetails] = useState("");
  // Loading & error state
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    setResult("");

    const payload = {
      task: selectedTask,
      user_input: userInput,
      additional_context_query: additionalContextQuery,
      include_latest_news: true,
      temperature,
      max_tokens: maxTokens,
      portfolio_details: portfolioDetails,
      domain_details: domainDetails,
      domain_type: domainType
    };

    try {
      const response = await axios.post('http://localhost:8000/api/analyze', payload);
      setResult(response.data.result);
      // Save history item with timestamp and details
      addHistoryItem({
        timestamp: new Date().toLocaleString(),
        task: selectedTask,
        query: selectedTask === "generic" ? userInput 
               : selectedTask === "portfolio" ? `Portfolio: ${portfolioDetails}\nQuery: ${userInput}`
               : `Holdings: ${domainDetails}\nQuery: ${userInput}`,
        response: response.data.result
      });
    } catch (err) {
      setError("Error occurred while fetching advice.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="advice-form">
      <h2>
        {selectedTask === "generic"
          ? "Generic Financial Advice"
          : selectedTask === "portfolio"
          ? "Portfolio Management"
          : "Domain-Specific Investment Advice"}
      </h2>
      <form onSubmit={handleSubmit}>
        {selectedTask === "portfolio" && (
          <>
            <label>Portfolio Details</label>
            <textarea
              placeholder="e.g., Stocks 60% (Tech 30%, Finance 20%, Healthcare 10%), Bonds 30%, Cash 10%"
              value={portfolioDetails}
              onChange={(e) => setPortfolioDetails(e.target.value)}
              required
            />
          </>
        )}
        {selectedTask === "domain" && (
          <>
            <label>Domain Type</label>
            <select value={domainType} onChange={(e) => setDomainType(e.target.value)}>
              <option value="Tech Stocks">Tech Stocks</option>
              <option value="Cryptocurrency">Cryptocurrency</option>
              <option value="Real Estate">Real Estate</option>
              <option value="Commodities">Commodities</option>
              <option value="ETFs & Mutual Funds">ETFs & Mutual Funds</option>
              <option value="Other">Other</option>
            </select>
            <label>Domain Holdings Details</label>
            <textarea
              placeholder="e.g., I own Bitcoin (30%), Ethereum (40%), and Solana (30%)"
              value={domainDetails}
              onChange={(e) => setDomainDetails(e.target.value)}
              required
            />
          </>
        )}
        <label>Your Query</label>
        <textarea
          placeholder="Describe your situation or ask your question..."
          value={userInput}
          onChange={(e) => setUserInput(e.target.value)}
          required
        />
        <label>Additional Context Query (optional)</label>
        <input
          type="text"
          placeholder="Enter keywords for extra context..."
          value={additionalContextQuery}
          onChange={(e) => setAdditionalContextQuery(e.target.value)}
        />
        <label>AI Creativity (Temperature): {temperature}</label>
        <input
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
        />
        <label>Response Length (Max Tokens): {maxTokens}</label>
        <input
          type="range"
          min="256"
          max="4096"
          step="256"
          value={maxTokens}
          onChange={(e) => setMaxTokens(parseInt(e.target.value))}
        />
        <button type="submit">{loading ? "Analyzing..." : "Get Advice"}</button>
        {error && <p className="error">{error}</p>}
        {result && (
          <div className="result">
            <h3>Advice:</h3>
            <pre>{result}</pre>
          </div>
        )}
      </form>
    </div>
  );
};

export default AdviceForm;