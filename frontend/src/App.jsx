// src/App.jsx
import React, { useState } from "react";
import UploadTest from "./components/UploadTest";
import TrendList from "./components/TrendList";
import TrendChart from "./components/TrendChart";
import "./App.css";

function App() {
  const [trends, setTrends] = useState([]);
  const [selectedTrend, setSelectedTrend] = useState(null);

  return (
    <div className="App">
      <h1>Trend Detection System</h1>
      <UploadTest onResults={setTrends} />
      <div className="layout">
        <TrendList trends={trends} onSelect={setSelectedTrend} />
        <TrendChart trend={selectedTrend} />
      </div>
    </div>
  );
}

export default App;
