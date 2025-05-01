// src/components/TrendList.jsx
import React from "react";
import "../styles/TrendList.css"; // Assuming you have some CSS for styling

function TrendList({ trends, onSelect }) {
  return (
    <div className="trend-list">
      <h3>Detected Trends ({trends.length})</h3>
      <ul>
        {trends.map((t, idx) => (
          <li key={idx}>
            <button onClick={() => onSelect(t)}>Trend #{idx + 1}</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default TrendList;
